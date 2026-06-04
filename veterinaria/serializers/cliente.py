from django.contrib.auth.models import User
from rest_framework import serializers
from veterinaria.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    user        = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, write_only=True,
    )
    username    = serializers.CharField(source='user.username', read_only=True)
    email       = serializers.EmailField(source='user.email', read_only=True)
    first_name  = serializers.CharField(source='user.first_name', read_only=True)
    last_name   = serializers.CharField(source='user.last_name', read_only=True)
    num_mascotas = serializers.SerializerMethodField()

    class Meta:
        model  = Cliente
        fields = [
            'id', 'user', 'username', 'email', 'first_name', 'last_name',
            'telefono', 'direccion', 'num_mascotas', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_num_mascotas(self, obj):
        return obj.mascotas.filter(is_active=True).count()
