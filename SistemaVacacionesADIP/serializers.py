from rest_framework import serializers
from .models import Area, Celula, Puesto, Empleado

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class CelulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celula
        fields = '__all__'

class PuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puesto
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

    def validate(self, data):
        area = data.get('area')
        celula = data.get('celula')

        if celula and celula.area != area:
            raise serializers.ValidationError(
                "La celula no pertenece al area asignada."
            )

        return data
