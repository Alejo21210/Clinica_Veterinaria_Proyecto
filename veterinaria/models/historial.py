from django.db import models
from .mascota      import Mascota
from .veterinario  import Veterinario


class HistorialMedico(models.Model):
    mascota       = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historial')
    veterinario   = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, related_name='registros')
    fecha         = models.DateTimeField(auto_now_add=True)
    diagnostico   = models.TextField()
    tratamiento   = models.TextField(blank=True, default='')
    observaciones = models.TextField(blank=True, default='')

    class Meta:
        verbose_name        = 'Historial Médico'
        verbose_name_plural = 'Historiales Médicos'
        ordering            = ['-fecha']

    def __str__(self):
        return f'{self.mascota.nombre} — {self.fecha.strftime("%d/%m/%Y %H:%M")}'
