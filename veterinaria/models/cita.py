from django.db import models
from .mascota      import Mascota
from .veterinario  import Veterinario


class Cita(models.Model):
    ESTADOS = [
        ('pendiente',  'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_curso',   'En Curso'),
        ('completada', 'Completada'),
        ('cancelada',  'Cancelada'),
    ]

    mascota      = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    veterinario  = models.ForeignKey(Veterinario, on_delete=models.CASCADE, related_name='citas')
    fecha        = models.DateField()
    hora         = models.TimeField()
    motivo       = models.TextField()
    estado       = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas        = models.TextField(blank=True, default='')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Cita'
        verbose_name_plural = 'Citas'
        ordering            = ['-fecha', '-hora']

    def __str__(self):
        return f'{self.mascota.nombre} con Dr. {self.veterinario.nombre} — {self.fecha} {self.hora}'
