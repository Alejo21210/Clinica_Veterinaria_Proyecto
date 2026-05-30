from rest_framework import serializers
from veterinaria.models import HistorialMedico
from veterinaria.serializers.mascota import MascotaSummarySerializer
from veterinaria.serializers.veterinario import VeterinarioSerializer


class HistorialMedicoSerializer(serializers.ModelSerializer):
    mascota_detalle     = MascotaSummarySerializer(source='mascota', read_only=True)
    veterinario_nombre  = serializers.CharField(source='veterinario.nombre', read_only=True)

    class Meta:
        model  = HistorialMedico
        fields = [
            'id', 'mascota', 'mascota_detalle',
            'veterinario', 'veterinario_nombre',
            'fecha', 'diagnostico', 'tratamiento', 'observaciones',
        ]
        read_only_fields = ['id', 'fecha']
