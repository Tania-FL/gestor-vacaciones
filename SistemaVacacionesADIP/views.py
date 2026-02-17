from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Area, Celula, Puesto, Empleado
from .serializers import AreaSerializer, CelulaSerializer, PuestoSerializer, EmpleadoSerializer


class AreaViewSet(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class CelulaViewSet(ModelViewSet):
    queryset = Celula.objects.all()
    serializer_class = CelulaSerializer

class PuestoViewSet(ModelViewSet):
    queryset = Puesto.objects.all()
    serializer_class = PuestoSerializer

class EmpleadoViewSet(ModelViewSet):
    queryset = Empleado.objects.select_related(
        'area', 'puesto', 'celula', 'jefe_directo'
    )
    serializer_class = EmpleadoSerializer