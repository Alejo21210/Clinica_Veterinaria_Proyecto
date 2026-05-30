from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from veterinaria.models               import HistorialMedico
from veterinaria.serializers.historial import HistorialMedicoSerializer
from veterinaria.permissions          import IsStaffOrReadOnly
from veterinaria.pagination           import StandardPagination


class HistorialMedicoViewSet(viewsets.ModelViewSet):
    serializer_class   = HistorialMedicoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    ordering_fields    = ['fecha']
    ordering           = ['-fecha']

    def get_queryset(self):
        if self.request.user.is_staff:
            return HistorialMedico.objects.select_related(
                'mascota__cliente__user', 'veterinario'
            ).all()
        return HistorialMedico.objects.filter(
            mascota__cliente__user=self.request.user
        ).select_related('mascota', 'veterinario')
