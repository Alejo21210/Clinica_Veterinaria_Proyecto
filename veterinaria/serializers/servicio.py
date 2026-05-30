from rest_framework import serializers
from veterinaria.models import Servicio


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Servicio
        fields = [
            'id', 'nombre', 'descripcion', 'precio',
            'duracion_minutos', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor a 0.')
        return value
