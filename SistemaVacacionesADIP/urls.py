from rest_framework.routers import DefaultRouter

from SistemaVacacionesADIP.views import AreaViewSet, CelulaViewSet, PuestoViewSet, EmpleadoViewSet
from sistema_vacaciones_adip.urls import urlpatterns

router = DefaultRouter()
router.register(r'areas', AreaViewSet)
router.register(r'celulas', CelulaViewSet)
router.register(r'puestos', PuestoViewSet)
router.register(r'empleados', EmpleadoViewSet)

urlpatterns = router.urls