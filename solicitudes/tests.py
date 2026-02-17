from datetime import date

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import (
    PeriodoVacacional,
    SaldoVacaciones,
    TipoAusencia,
    EstadoSolicitud,
    SolicitudAusencia,
)

User = get_user_model()


class ChangeStatusSaldoValidationTests(TestCase):
    """Tests para validación de saldo en POST /api/requests/{id}/change-status/"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="aprobador", password="test123", email="aprobador@test.com"
        )
        self.empleado = User.objects.create_user(
            username="empleado", password="test123", email="empleado@test.com"
        )
        self.client.force_authenticate(user=self.user)

        self.periodo = PeriodoVacacional.objects.create(
            anio=2026,
            fecha_inicio=date(2026, 1, 1),
            fecha_fin=date(2026, 12, 31),
            activo=True,
        )
        self.tipo_vacaciones = TipoAusencia.objects.create(
            nombre="Vacaciones",
            descuenta_saldo=True,
            requiere_aprobacion=True,
        )
        # Crear estados en orden de IDs de producción: 1=Aprobada, 2=Pendiente, etc.
        self.estado_aprobada = EstadoSolicitud.objects.create(nombre="Aprobada")
        self.estado_pendiente = EstadoSolicitud.objects.create(nombre="Pendiente")

    def test_aprobar_con_saldo_insuficiente_retorna_400_y_no_cambia_estado(self):
        """Aprobar con más días solicitados que disponibles => 400 y estado permanece Pendiente."""
        saldo = SaldoVacaciones.objects.create(
            empleado=self.empleado,
            periodo=self.periodo,
            dias_generados=5,
            dias_usados=0,
            dias_pendientes=5,
        )
        solicitud = SolicitudAusencia.objects.create(
            empleado=self.empleado,
            tipo_ausencia=self.tipo_vacaciones,
            fecha_inicio=date(2026, 3, 1),
            fecha_fin=date(2026, 3, 10),
            dias_solicitados=10,  # Más que los 5 disponibles
            estado=self.estado_pendiente,
            fecha_solicitud=timezone.now(),
        )

        url = f"/api/requests/{solicitud.id}/change-status/"
        response = self.client.post(
            url,
            {"estado_id": self.estado_aprobada.id, "comentario": ""},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("Saldo insuficiente", response.data["error"])

        solicitud.refresh_from_db()
        self.assertEqual(solicitud.estado_id, self.estado_pendiente.id)

        saldo.refresh_from_db()
        self.assertEqual(saldo.dias_usados, 0)
        self.assertEqual(saldo.dias_pendientes, 5)

    def test_aprobar_con_saldo_suficiente_retorna_200_y_actualiza_saldo(self):
        """Aprobar con saldo suficiente => 200 y actualiza dias_usados y dias_pendientes."""
        saldo = SaldoVacaciones.objects.create(
            empleado=self.empleado,
            periodo=self.periodo,
            dias_generados=15,
            dias_usados=3,
            dias_pendientes=12,
        )
        solicitud = SolicitudAusencia.objects.create(
            empleado=self.empleado,
            tipo_ausencia=self.tipo_vacaciones,
            fecha_inicio=date(2026, 3, 1),
            fecha_fin=date(2026, 3, 5),
            dias_solicitados=5,
            estado=self.estado_pendiente,
            fecha_solicitud=timezone.now(),
        )

        url = f"/api/requests/{solicitud.id}/change-status/"
        response = self.client.post(
            url,
            {"estado_id": self.estado_aprobada.id, "comentario": "Aprobado"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        solicitud.refresh_from_db()
        self.assertEqual(solicitud.estado_id, self.estado_aprobada.id)

        saldo.refresh_from_db()
        self.assertEqual(saldo.dias_usados, 8)  # 3 + 5
        self.assertEqual(saldo.dias_pendientes, 7)  # 15 - 8
