from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from veterinaria.models               import Servicio
from veterinaria.serializers.servicio import ServicioSerializer
from veterinaria.permissions          import IsStaffOrReadOnly
from veterinaria.pagination           import StandardPagination


class ServicioViewSet(viewsets.ModelViewSet):
    queryset           = Servicio.objects.all()
    serializer_class   = ServicioSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields      = ['nombre', 'descripcion']
    ordering_fields    = ['nombre', 'precio', 'created_at']
    ordering           = ['nombre']

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Servicio.objects.all()
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(is_active=True).count(),
            'inactive': qs.filter(is_active=False).count(),
        })
