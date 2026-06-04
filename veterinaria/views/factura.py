from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum

from veterinaria.models              import Cliente, Factura, DetalleFactura, Servicio
from veterinaria.serializers.factura import FacturaSerializer, DetalleFacturaSerializer
from veterinaria.permissions         import IsOwnerOrStaff
from veterinaria.filters             import FacturaFilter
from veterinaria.pagination          import StandardPagination


class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class   = FacturaSerializer
    permission_classes = [IsOwnerOrStaff]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = FacturaFilter
    search_fields      = ['cliente__user__username', 'cliente__user__email']
    ordering_fields    = ['fecha', 'total']
    ordering           = ['-fecha']
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Factura.objects.select_related('cliente__user').prefetch_related(
                'detalles__servicio'
            ).all()
        return Factura.objects.filter(
            cliente__user=self.request.user
        ).prefetch_related('detalles__servicio')

    def perform_create(self, serializer):
        try:
            serializer.save(cliente=self.request.user.cliente)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError(
                {'cliente': 'El usuario autenticado no tiene un cliente asociado.'}
            )

    @action(detail=True, methods=['post'], url_path='agregar-servicio')
    def agregar_servicio(self, request, pk=None):
        factura = self.get_object()
        if factura.pagada:
            return Response(
                {'error': 'No se puede modificar una factura ya pagada.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        servicio_id = request.data.get('servicio_id')
        cantidad    = int(request.data.get('cantidad', 1))
        try:
            servicio = Servicio.objects.get(pk=servicio_id, is_active=True)
        except Servicio.DoesNotExist:
            return Response(
                {'error': 'Servicio no encontrado o inactivo.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        detalle, created = DetalleFactura.objects.get_or_create(
            factura=factura,
            servicio=servicio,
            defaults={'precio_unitario': servicio.precio, 'cantidad': cantidad},
        )
        if not created:
            detalle.cantidad += cantidad
            detalle.save(update_fields=['cantidad'])
        factura.calcular_total()
        return Response(FacturaSerializer(factura).data)

    @action(detail=True, methods=['post'], url_path='marcar-pagada')
    def marcar_pagada(self, request, pk=None):
        factura = self.get_object()
        if factura.pagada:
            return Response({'error': 'La factura ya está pagada.'}, status=status.HTTP_400_BAD_REQUEST)
        factura.pagada = True
        factura.save(update_fields=['pagada'])
        return Response(FacturaSerializer(factura).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser], url_path='stats')
    def stats(self, request):
        qs = Factura.objects.all()
        ingresos = qs.aggregate(total=Sum('total'))
        return Response({
            'total_facturas': qs.count(),
            'ingresos_total': float(ingresos['total'] or 0),
            'pagadas':        qs.filter(pagada=True).count(),
            'pendientes':     qs.filter(pagada=False).count(),
        })
