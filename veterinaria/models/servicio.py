from django.db import models


class Servicio(models.Model):
    nombre          = models.CharField(max_length=100, unique=True)
    descripcion     = models.TextField(blank=True, default='')
    precio          = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minutos = models.PositiveIntegerField(default=30)
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering            = ['nombre']

    def __str__(self):
        return f'{self.nombre} — ${self.precio}'
