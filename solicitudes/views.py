from django.shortcuts import render
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    TipoAusencia, EstadoSolicitud, CalendarioLaboral, 
    SolicitudAusencia, HistorialSolicitud
)
from .serializers import (
    TipoAusenciaSerializer, EstadoSolicitudSerializer, 
    CalendarioLaboralSerializer, SolicitudAusenciaSerializer, 
    HistorialSolicitudSerializer
)

class ReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """Base ViewSet for Catalog tables"""
    pass

class TipoAusenciaViewSet(ReadOnlyViewSet):
    queryset = TipoAusencia.objects.filter(activo=True)
    serializer_class = TipoAusenciaSerializer

class EstadoSolicitudViewSet(ReadOnlyViewSet):
    queryset = EstadoSolicitud.objects.all()
    serializer_class = EstadoSolicitudSerializer

class CalendarioLaboralViewSet(ReadOnlyViewSet):
    queryset = CalendarioLaboral.objects.all()
    serializer_class = CalendarioLaboralSerializer

class SolicitudAusenciaViewSet(viewsets.ModelViewSet):
    queryset = SolicitudAusencia.objects.all()
    serializer_class = SolicitudAusenciaSerializer
    def perform_create(self, serializer):
        # Asignar estado por defecto al crear (ej. "Pendiente")
        pendiente = EstadoSolicitud.objects.filter(nombre__iexact="Pendiente").first()

        # Si no existe "Pendiente", usa el primer estado disponible para no tronar
        if pendiente is None:
            pendiente = EstadoSolicitud.objects.first()

        serializer.save(estado=pendiente)   

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        solicitud = self.get_object()
        historial = solicitud.historial.all().order_by('-fecha_cambio')
        serializer = HistorialSolicitudSerializer(historial, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        solicitud = self.get_object()
        nuevo_estado_id = request.data.get('estado_id')
        comentario = request.data.get('comentario', '')

        if not nuevo_estado_id:
            return Response({"error": "estado_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nuevo_estado = EstadoSolicitud.objects.get(id=nuevo_estado_id)
        except EstadoSolicitud.DoesNotExist:
            return Response({"error": "Invalid state ID"}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            estado_anterior = solicitud.estado
            
            # Update request
            solicitud.estado = nuevo_estado
            solicitud.fecha_respuesta = timezone.now()
            solicitud.comentario_aprobador = comentario
            solicitud.save()

            # Create history record
            HistorialSolicitud.objects.create(
                solicitud=solicitud,
                estado_anterior=estado_anterior,
                estado_nuevo=nuevo_estado,
                usuario=request.user,
                comentario=comentario,
                fecha_cambio=timezone.now()
            )

        return Response(self.get_serializer(solicitud).data)

