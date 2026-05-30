from rest_framework import serializers
from veterinaria.models import Mascota


class MascotaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.user.username', read_only=True)
    edad           = serializers.SerializerMethodField()

    class Meta:
        model  = Mascota
        fields = [
            'id', 'nombre', 'especie', 'raza',
            'fecha_nacimiento', 'edad', 'peso',
            'cliente', 'cliente_nombre',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_edad(self, obj):
        if obj.fecha_nacimiento:
            from datetime import date
            today = date.today()
            edad = today.year - obj.fecha_nacimiento.year
            if (today.month, today.day) < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day):
                edad -= 1
            return edad
        return None


class MascotaSummarySerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.user.username', read_only=True)

    class Meta:
        model  = Mascota
        fields = ['id', 'nombre', 'especie', 'raza', 'cliente_nombre', 'is_active']
