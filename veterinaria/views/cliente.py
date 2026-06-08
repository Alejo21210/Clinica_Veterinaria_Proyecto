from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db import IntegrityError

from veterinaria.models              import Cliente
from veterinaria.serializers.cliente import ClienteSerializer
from veterinaria.pagination          import StandardPagination


class ClienteViewSet(viewsets.ModelViewSet):
    queryset           = Cliente.objects.select_related('user').all()
    serializer_class   = ClienteSerializer
    permission_classes = [IsAdminUser]
    pagination_class   = StandardPagination
    search_fields      = ['user__username', 'user__email', 'telefono']
    ordering_fields    = ['id', 'user__username', 'created_at']
    ordering           = ['id']

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        if user_id:
            if Cliente.objects.filter(user_id=user_id).exists():
                raise serializers.ValidationError(
                    {'user': 'Este usuario ya tiene un cliente asignado.'}
                )
            serializer.save(user_id=user_id)
        else:
            if Cliente.objects.filter(user=self.request.user).exists():
                raise serializers.ValidationError(
                    {'user': 'Este usuario ya tiene un cliente asignado.'}
                )
            serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            return Response(
                {'error': 'El usuario ya tiene un cliente asignado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = self.get_queryset()
        return Response({
            'total':         qs.count(),
            'con_mascotas':  qs.filter(mascotas__isnull=False).distinct().count(),
        })
