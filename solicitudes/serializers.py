from decimal import Decimal

from rest_framework import serializers

from .models import (
    TipoAusencia, EstadoSolicitud, CalendarioLaboral,
    SolicitudAusencia, HistorialSolicitud
)
from .services import calcular_dias_habiles

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
    dias_calculados = serializers.SerializerMethodField(read_only=True)

    def get_dias_calculados(self, obj):
        return Decimal(calcular_dias_habiles(obj.fecha_inicio, obj.fecha_fin)).quantize(Decimal("0.00"))

    def validate(self, attrs):
        """Validate that dias_solicitados matches the business days calculation."""
        fecha_inicio = attrs.get('fecha_inicio') or (self.instance and self.instance.fecha_inicio)
        fecha_fin = attrs.get('fecha_fin') or (self.instance and self.instance.fecha_fin)
        dias_solicitados = attrs.get('dias_solicitados')

        if fecha_inicio and fecha_fin and dias_solicitados is not None:
            dias_calculados = calcular_dias_habiles(fecha_inicio, fecha_fin)
            dias_solicitados_decimal = Decimal(str(dias_solicitados))

            if dias_solicitados_decimal != dias_calculados:
                raise serializers.ValidationError({
                    'dias_solicitados': (
                        f'Los días solicitados ({dias_solicitados}) no coinciden con '
                        f'los días hábiles del rango ({dias_calculados}). '
                        'Verifique las fechas y el calendario laboral.'
                    )
                })

        return attrs

    class Meta:
        model = SolicitudAusencia
        fields = [
            'id', 'empleado', 'tipo_ausencia', 'fecha_inicio', 'fecha_fin',
            'dias_solicitados', 'dias_calculados', 'estado', 'motivo',
            'comentario_aprobador', 'fecha_solicitud', 'fecha_respuesta',
            'created_at', 'updated_at',
            'estado_nombre', 'tipo_ausencia_nombre',
        ]
        read_only_fields = ['estado', 'fecha_respuesta']