from django.contrib import admin

from .models import (
    PeriodoVacacional,
    TipoAusencia,
    EstadoSolicitud,
    SaldoVacaciones,
    TipoDiaCalendario,
    CalendarioLaboral,
    SolicitudAusencia,
    HistorialSolicitud,
)


@admin.register(PeriodoVacacional)
class PeriodoVacacionalAdmin(admin.ModelAdmin):
    list_display = ("anio", "fecha_inicio", "fecha_fin", "activo")
    list_filter = ("activo",)
    search_fields = ("anio",)


@admin.register(TipoAusencia)
class TipoAusenciaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "requiere_aprobacion", "descuenta_saldo", "activo")
    list_filter = ("activo", "requiere_aprobacion")
    search_fields = ("nombre",)


@admin.register(EstadoSolicitud)
class EstadoSolicitudAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(SaldoVacaciones)
class SaldoVacacionesAdmin(admin.ModelAdmin):
    list_display = (
        "empleado",
        "periodo",
        "dias_generados",
        "dias_usados",
        "dias_pendientes",
    )
    list_filter = ("periodo",)
    search_fields = ("empleado__username",)


@admin.register(TipoDiaCalendario)
class TipoDiaCalendarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "es_laborable")
    list_filter = ("es_laborable",)
    search_fields = ("nombre",)


@admin.register(CalendarioLaboral)
class CalendarioLaboralAdmin(admin.ModelAdmin):
    list_display = ("fecha", "tipo_dia", "descripcion")
    list_filter = ("tipo_dia",)
    search_fields = ("fecha",)


@admin.register(SolicitudAusencia)
class SolicitudAusenciaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "empleado",
        "tipo_ausencia",
        "estado",
        "fecha_inicio",
        "fecha_fin",
        "dias_solicitados",
    )
    list_filter = ("estado", "tipo_ausencia")
    search_fields = ("empleado__username",)


@admin.register(HistorialSolicitud)
class HistorialSolicitudAdmin(admin.ModelAdmin):
    list_display = (
        "solicitud",
        "estado_anterior",
        "estado_nuevo",
        "usuario",
        "fecha_cambio",
    )
    list_filter = ("estado_nuevo",)
