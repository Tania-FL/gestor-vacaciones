"""
Servicio para el consumo de saldo de vacaciones al aprobar solicitudes.
"""
from typing import Optional

from ..models import SaldoVacaciones, PeriodoVacacional, SolicitudAusencia


class SaldoInsuficienteError(Exception):
    """Error cuando no hay saldo suficiente para aprobar la solicitud."""

    def __init__(self, message: str = "Saldo insuficiente"):
        self.message = message
        super().__init__(message)


def consumir_saldo_al_aprobar(solicitud: SolicitudAusencia) -> None:
    """
    Consume el saldo de vacaciones cuando una SolicitudAusencia es aprobada.

    Solo aplica si tipo_ausencia.descuenta_saldo es True.

    Reglas:
    - Valida: solicitud.dias_solicitados <= saldo.dias_disponibles
    - Incrementa saldo.dias_usados en solicitud.dias_solicitados
    - Recalcula y guarda saldo.dias_pendientes = dias_generados - dias_usados

    Raises:
        SaldoInsuficienteError: Si no hay saldo suficiente o no existe saldo.
    """
    if not solicitud.tipo_ausencia.descuenta_saldo:
        return

    periodo = _obtener_periodo_para_solicitud(solicitud)
    if periodo is None:
        raise SaldoInsuficienteError()

    try:
        saldo = SaldoVacaciones.objects.get(
            empleado=solicitud.empleado,
            periodo=periodo,
        )
    except SaldoVacaciones.DoesNotExist:
        raise SaldoInsuficienteError()

    dias_disponibles = saldo.dias_disponibles
    if solicitud.dias_solicitados > dias_disponibles:
        raise SaldoInsuficienteError()

    # Incrementar dias_usados (fuente primaria de consumo)
    saldo.dias_usados += solicitud.dias_solicitados
    # Recalcular dias_pendientes
    saldo.dias_pendientes = saldo.dias_generados - saldo.dias_usados
    saldo.save()


def _obtener_periodo_para_solicitud(solicitud: SolicitudAusencia) -> Optional[PeriodoVacacional]:
    """
    Obtiene el PeriodoVacacional que contiene la fecha_inicio de la solicitud.
    """
    return (
        PeriodoVacacional.objects.filter(
            fecha_inicio__lte=solicitud.fecha_inicio,
            fecha_fin__gte=solicitud.fecha_inicio,
        )
        .first()
    )
