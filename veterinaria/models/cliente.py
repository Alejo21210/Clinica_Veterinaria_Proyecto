from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    telefono  = models.CharField(max_length=20)
    direccion = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering            = ['user__username']

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} — {self.telefono}'
