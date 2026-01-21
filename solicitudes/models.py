from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# =========================
# CATÁLOGOS / BASE
# =========================

class PeriodoVacacional(models.Model):
    """
    Ej: 2026 (inicio-fin del periodo de vacaciones)
    """
    anio = models.PositiveIntegerField(unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Periodo {self.anio}"


class TipoAusencia(models.Model):
    """
    Ej: Vacaciones, Permiso, Incapacidad, Comisión, etc.
    """
    nombre = models.CharField(max_length=100, unique=True)
    requiere_aprobacion = models.BooleanField(default=True)
    descuenta_saldo = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class EstadoSolicitud(models.Model):
    """
    Ej: Pendiente, Aprobada, Rechazada, Cancelada
    """
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


# =========================
# SALDOS
# =========================

class SaldoVacaciones(TimeStampedModel):
    """
    Saldo de vacaciones por empleado y periodo.
    NOTA: aquí uso FK a 'empleados.Empleado'. Si tu app se llama diferente,
    lo cambiamos (por ejemplo 'usuarios.Empleado' o lo que tengan ustedes).
    SE COLOCO settings.AUTH_USER_MODEL en el lugar de la ForeignKey para que funcione con el modelo de usuario personalizado. Entonces cuando este el
    modelo empleado, ya se cambie settings.AUTH_USER_MODEL por 'empleados.Empleado'.
    """
    empleado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="saldos_vacaciones",
    )
    periodo = models.ForeignKey(
        PeriodoVacacional,
        on_delete=models.PROTECT,
        related_name="saldos",
    )

    dias_generados = models.DecimalField(max_digits=5, decimal_places=2)
    dias_usados = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dias_pendientes = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["empleado", "periodo"],
                name="unique_saldo_por_empleado_periodo",
            )
        ]

    def __str__(self):
        return f"Saldo {self.empleado_id} - {self.periodo.anio}"


# =========================
# CALENDARIO
# =========================

class TipoDiaCalendario(models.Model):
    """
    Ej: Laborable, Festivo, Fin de semana
    """
    nombre = models.CharField(max_length=50, unique=True)
    es_laborable = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class CalendarioLaboral(models.Model):
    fecha = models.DateField(unique=True)
    tipo_dia = models.ForeignKey(
        TipoDiaCalendario,
        on_delete=models.PROTECT,
        related_name="fechas",
    )
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.fecha} - {self.tipo_dia.nombre}"


# =========================
# SOLICITUDES + HISTORIAL
# =========================

class SolicitudAusencia(TimeStampedModel):
    empleado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="solicitudes",
    )
    tipo_ausencia = models.ForeignKey(
        TipoAusencia,
        on_delete=models.PROTECT,
        related_name="solicitudes",
    )

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dias_solicitados = models.DecimalField(max_digits=5, decimal_places=2)

    estado = models.ForeignKey(
        EstadoSolicitud,
        on_delete=models.PROTECT,
        related_name="solicitudes",
    )

    motivo = models.TextField(blank=True, null=True)
    comentario_aprobador = models.TextField(blank=True, null=True)

    fecha_solicitud = models.DateTimeField()
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Solicitud #{self.id} ({self.empleado_id})"


class HistorialSolicitud(models.Model):
    solicitud = models.ForeignKey(
        SolicitudAusencia,
        on_delete=models.CASCADE,
        related_name="historial",
    )
    estado_anterior = models.ForeignKey(
        EstadoSolicitud,
        on_delete=models.PROTECT,
        related_name="historiales_como_anterior",
    )
    estado_nuevo = models.ForeignKey(
        EstadoSolicitud,
        on_delete=models.PROTECT,
        related_name="historiales_como_nuevo",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="cambios_solicitudes",
    )
    comentario = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField()

    def __str__(self):
        return f"Historial #{self.id} - Solicitud {self.solicitud_id}"
