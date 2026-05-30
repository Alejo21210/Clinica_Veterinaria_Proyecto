from rest_framework import serializers
from veterinaria.models import Cita
from veterinaria.serializers.mascota import MascotaSummarySerializer
from veterinaria.serializers.veterinario import VeterinarioSerializer


class CitaSerializer(serializers.ModelSerializer):
    mascota_detalle     = MascotaSummarySerializer(source='mascota', read_only=True)
    veterinario_detalle = VeterinarioSerializer(source='veterinario', read_only=True)

    class Meta:
        model  = Cita
        fields = [
            'id', 'mascota', 'mascota_detalle',
            'veterinario', 'veterinario_detalle',
            'fecha', 'hora', 'motivo', 'estado', 'notas',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
