from rest_framework import serializers
from .models import (
    TipoAusencia, EstadoSolicitud, CalendarioLaboral, 
    SolicitudAusencia, HistorialSolicitud
)

class TipoAusenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAusencia
        fields = '__all__'

class EstadoSolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoSolicitud
        fields = '__all__'

class CalendarioLaboralSerializer(serializers.ModelSerializer):
    tipo_dia_nombre = serializers.CharField(source='tipo_dia.nombre', read_only=True)
    class Meta:
        model = CalendarioLaboral
        fields = ['id', 'fecha', 'tipo_dia', 'tipo_dia_nombre', 'descripcion']

class HistorialSolicitudSerializer(serializers.ModelSerializer):
    estado_anterior_nombre = serializers.CharField(source='estado_anterior.nombre', read_only=True)
    estado_nuevo_nombre = serializers.CharField(source='estado_nuevo.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)

    class Meta:
        model = HistorialSolicitud
        fields = '__all__'

class SolicitudAusenciaSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    tipo_ausencia_nombre = serializers.CharField(source='tipo_ausencia.nombre', read_only=True)
    
    class Meta:
        model = SolicitudAusencia
        fields = '__all__'
        read_only_fields = ['estado', 'fecha_respuesta']