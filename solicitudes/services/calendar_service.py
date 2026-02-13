"""
Calendar service for business days calculation.
"""
from datetime import date, timedelta

from ..models import CalendarioLaboral


def calcular_dias_habiles(fecha_inicio: date, fecha_fin: date) -> int:
    """
    Calculate the number of working days between two dates (inclusive).

    Uses CalendarioLaboral and TipoDiaCalendario.es_laborable to determine
    if each date is a working day. If a date is not in CalendarioLaboral,
    Saturday (6) and Sunday (5) are treated as non-working days.

    Args:
        fecha_inicio: Start date (inclusive).
        fecha_fin: End date (inclusive).

    Returns:
        Total number of working days in the range.
    """
    if fecha_inicio > fecha_fin:
        return 0

    # Prefetch all calendar entries for the date range to avoid N+1 queries
    calendar_entries = {
        entry.fecha: entry.tipo_dia.es_laborable
        for entry in CalendarioLaboral.objects.filter(
            fecha__gte=fecha_inicio,
            fecha__lte=fecha_fin
        ).select_related('tipo_dia')
    }

    working_days = 0
    current = fecha_inicio

    while current <= fecha_fin:
        if current in calendar_entries:
            if calendar_entries[current]:
                working_days += 1
        else:
            # Not in calendar: Saturday (5) and Sunday (6) are non-working
            if current.weekday() < 5:
                working_days += 1

        current += timedelta(days=1)

    return working_days
