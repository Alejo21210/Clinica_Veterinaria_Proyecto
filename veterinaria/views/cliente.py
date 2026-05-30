from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

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

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = self.get_queryset()
        return Response({
            'total':         qs.count(),
            'con_mascotas':  qs.filter(mascotas__isnull=False).distinct().count(),
        })
