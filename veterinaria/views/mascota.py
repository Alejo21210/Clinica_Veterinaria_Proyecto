from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from veterinaria.models             import Mascota
from veterinaria.serializers.mascota import MascotaSerializer, MascotaSummarySerializer
from veterinaria.permissions        import IsStaffOrReadOnly
from veterinaria.filters            import MascotaFilter
from veterinaria.pagination         import StandardPagination


class MascotaViewSet(viewsets.ModelViewSet):
    queryset           = Mascota.objects.select_related('cliente__user').all()
    serializer_class   = MascotaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = MascotaFilter
    search_fields      = ['nombre', 'raza', 'cliente__user__username']
    ordering_fields    = ['nombre', 'created_at']
    ordering           = ['nombre']

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = Mascota.objects.all()
        return Response({
            'total':      qs.count(),
            'active':     qs.filter(is_active=True).count(),
            'por_especie': dict(
                qs.values('especie').annotate(total=Count('id'))
                .values_list('especie', 'total')
            ),
        })
