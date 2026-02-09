from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TipoAusenciaViewSet, EstadoSolicitudViewSet, 
    CalendarioLaboralViewSet, SolicitudAusenciaViewSet
)

router = DefaultRouter()
router.register(r'absence-types', TipoAusenciaViewSet)
router.register(r'statuses', EstadoSolicitudViewSet)
router.register(r'calendar', CalendarioLaboralViewSet)
router.register(r'requests', SolicitudAusenciaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]