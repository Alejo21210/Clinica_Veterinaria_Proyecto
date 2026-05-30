from django.db import models
from .cliente   import Cliente
from .servicio  import Servicio


class Factura(models.Model):
    cliente    = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='facturas')
    servicios  = models.ManyToManyField(Servicio, through='DetalleFactura', related_name='facturas')
    fecha      = models.DateTimeField(auto_now_add=True)
    total      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pagada     = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering            = ['-fecha']

    def __str__(self):
        return f'Factura #{self.id} — {self.cliente} — ${self.total}'

    def calcular_total(self):
        self.total = sum(
            item.subtotal
            for item in self.detalles.all()
        )
        self.save(update_fields=['total'])


class DetalleFactura(models.Model):
    factura         = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    servicio        = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    cantidad        = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name        = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Factura'

    @property
    def subtotal(self):
        return float(self.precio_unitario) * self.cantidad

    def __str__(self):
        return f'{self.cantidad}x {self.servicio.nombre}'
