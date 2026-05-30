from django.db import models
from django.contrib.auth.models import User


class Veterinario(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='veterinario', null=True, blank=True)
    nombre          = models.CharField(max_length=100)
    especialidad    = models.CharField(max_length=100)
    telefono        = models.CharField(max_length=20)
    email           = models.EmailField()
    horario_atencion = models.CharField(max_length=200, blank=True, default='')
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Veterinario'
        verbose_name_plural = 'Veterinarios'
        ordering            = ['nombre']

    def __str__(self):
        return f'Dr. {self.nombre} — {self.especialidad}'
