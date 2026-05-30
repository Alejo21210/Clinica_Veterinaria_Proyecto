from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from veterinaria.models                import Veterinario
from veterinaria.serializers.veterinario import VeterinarioSerializer
from veterinaria.permissions           import IsStaffOrReadOnly
from veterinaria.pagination            import StandardPagination


class VeterinarioViewSet(viewsets.ModelViewSet):
    queryset           = Veterinario.objects.all()
    serializer_class   = VeterinarioSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields      = ['nombre', 'especialidad', 'email']
    ordering_fields    = ['nombre', 'especialidad', 'created_at']
    ordering           = ['nombre']

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Veterinario.objects.all()
        return Response({
            'total':            qs.count(),
            'active':           qs.filter(is_active=True).count(),
            'por_especialidad': dict(
                qs.values('especialidad').annotate(total=Count('id'))
                .values_list('especialidad', 'total')
            ),
        })
