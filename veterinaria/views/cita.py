from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from veterinaria.models          import Cita
from veterinaria.serializers.cita import CitaSerializer
from veterinaria.permissions     import IsStaffOrReadOnly
from veterinaria.filters         import CitaFilter
from veterinaria.pagination      import StandardPagination


class CitaViewSet(viewsets.ModelViewSet):
    serializer_class   = CitaSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = CitaFilter
    ordering_fields    = ['fecha', 'hora', 'created_at']
    ordering           = ['-fecha', '-hora']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Cita.objects.select_related(
                'mascota__cliente__user', 'veterinario'
            ).all()
        return Cita.objects.filter(
            mascota__cliente__user=self.request.user
        ).select_related('mascota', 'veterinario')

    @action(
        detail=True, methods=['post'],
        url_path='cambiar-estado',
    )
    def cambiar_estado(self, request, pk=None):
        cita = self.get_object()
        nuevo_estado = request.data.get('estado')
        estados_validos = [s[0] for s in Cita.ESTADOS]
        if nuevo_estado not in estados_validos:
            return Response(
                {'error': f'Estado inválido. Opciones: {estados_validos}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cita.estado = nuevo_estado
        cita.save(update_fields=['estado'])
        return Response(CitaSerializer(cita).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser], url_path='stats')
    def stats(self, request):
        qs = Cita.objects.all()
        return Response({
            'total':     qs.count(),
            'por_estado': dict(
                qs.values('estado').annotate(total=Count('id'))
                .values_list('estado', 'total')
            ),
        })
