from django.db import models
from .cliente import Cliente


class Mascota(models.Model):
    ESPECIES = [
        ('perro', 'Perro'),
        ('gato',  'Gato'),
        ('ave',   'Ave'),
        ('conejo','Conejo'),
        ('otro',  'Otro'),
    ]

    nombre           = models.CharField(max_length=100)
    especie          = models.CharField(max_length=20, choices=ESPECIES)
    raza             = models.CharField(max_length=100, blank=True, default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso             = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cliente          = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas')
    is_active        = models.BooleanField(default=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering            = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.get_especie_display()})'
