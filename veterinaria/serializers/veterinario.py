from rest_framework import serializers
from veterinaria.models import Veterinario


class VeterinarioSerializer(serializers.ModelSerializer):
    num_citas = serializers.SerializerMethodField()

    class Meta:
        model  = Veterinario
        fields = [
            'id', 'nombre', 'especialidad', 'telefono', 'email',
            'horario_atencion', 'is_active', 'num_citas', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_num_citas(self, obj):
        return obj.citas.count()
