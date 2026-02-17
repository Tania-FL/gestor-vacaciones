"""
Servicio para el consumo y reversión de saldo de vacaciones al cambiar estado de solicitudes.
"""
from typing import Optional

from ..models import SaldoVacaciones, PeriodoVacacional, SolicitudAusencia, EstadoSolicitud


class SaldoInsuficienteError(Exception):
    """Error cuando no hay saldo suficiente para aprobar la solicitud."""

    def __init__(self, message: str = "Saldo insuficiente"):
        self.message = message
        super().__init__(message)


class SaldoNoExisteError(Exception):
    """Error cuando no existe saldo de vacaciones para el empleado en el periodo vigente."""

    def __init__(self, message: str = "No existe saldo de vacaciones para el empleado en el periodo vigente"):
        self.message = message
        super().__init__(message)


def _obtener_periodo_para_solicitud(solicitud: SolicitudAusencia) -> Optional[PeriodoVacacional]:
    """
    Obtiene el PeriodoVacacional activo que contiene la fecha_inicio de la solicitud.
    """
    return (
        PeriodoVacacional.objects.filter(
            activo=True,
            fecha_inicio__lte=solicitud.fecha_inicio,
            fecha_fin__gte=solicitud.fecha_inicio,
        )
        .first()
    )


def consumir_saldo_al_aprobar(solicitud: SolicitudAusencia) -> None:
    """
    Consume el saldo de vacaciones cuando una SolicitudAusencia es aprobada.

    Solo aplica si tipo_ausencia.descuenta_saldo es True.

    Reglas:
    1. Buscar PeriodoVacacional activo que contenga fecha_inicio.
    2. Obtener SaldoVacaciones del empleado para ese periodo.
    3. Validar: solicitud.dias_solicitados <= saldo.dias_disponibles
    4. Incrementa saldo.dias_usados y recalcula saldo.dias_pendientes

    Raises:
        SaldoNoExisteError: Si no existe periodo o saldo.
        SaldoInsuficienteError: Si no hay saldo suficiente.
    """
    if not solicitud.tipo_ausencia.descuenta_saldo:
        return

    periodo = _obtener_periodo_para_solicitud(solicitud)
    if periodo is None:
        raise SaldoNoExisteError(
            "No existe periodo vacacional activo para la fecha de la solicitud"
        )

    try:
        saldo = SaldoVacaciones.objects.get(
            empleado=solicitud.empleado,
            periodo=periodo,
        )
    except SaldoVacaciones.DoesNotExist:
        raise SaldoNoExisteError(
            "No eimage.pngxiste saldo de vacaciones para el empleado en el periodo vigente"
        )

    dias_disponibles = saldo.dias_disponibles
    if solicitud.dias_solicitados > dias_disponibles:
        raise SaldoInsuficienteError("Saldo insuficiente")

    saldo.dias_usados += solicitud.dias_solicitados
    saldo.dias_pendientes = saldo.dias_generados - saldo.dias_usados
    saldo.save()


def revertir_saldo_al_cancelar_o_rechazar(
    solicitud: SolicitudAusencia,
    estado_anterior: EstadoSolicitud,
) -> None:
    """
    Revierte el consumo de saldo cuando una solicitud aprobada pasa a Cancelada o Rechazada.

    Solo aplica si:
    - estado_anterior era Aprobada
    - tipo_ausencia.descuenta_saldo es True
    - Existe el saldo (evita negativos en dias_usados)
    """
    if not estado_anterior.nombre or estado_anterior.nombre.lower() != "aprobada":
        return
    if not solicitud.tipo_ausencia.descuenta_saldo:
        return

    periodo = _obtener_periodo_para_solicitud(solicitud)
    if periodo is None:
        return

    try:
        saldo = SaldoVacaciones.objects.get(
            empleado=solicitud.empleado,
            periodo=periodo,
        )
    except SaldoVacaciones.DoesNotExist:
        return

    dias_a_revertir = min(solicitud.dias_solicitados, saldo.dias_usados)
    saldo.dias_usados = saldo.dias_usados - dias_a_revertir
    saldo.dias_pendientes = saldo.dias_generados - saldo.dias_usados
    saldo.save()
