from django.contrib import admin
from veterinaria.models import (
    Cliente, Mascota, Veterinario, Cita,
    HistorialMedico, Servicio, Factura, DetalleFactura,
)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'telefono', 'created_at']
    search_fields = ['user__username', 'user__email', 'telefono']


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'especie', 'raza', 'cliente', 'is_active']
    list_filter   = ['especie', 'is_active']
    search_fields = ['nombre', 'raza', 'cliente__user__username']


@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'especialidad', 'telefono', 'is_active']
    list_filter   = ['especialidad', 'is_active']
    search_fields = ['nombre', 'especialidad', 'email']


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'mascota', 'veterinario', 'fecha', 'hora', 'estado']
    list_filter   = ['estado', 'fecha']
    search_fields = ['mascota__nombre', 'veterinario__nombre']


@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'mascota', 'veterinario', 'fecha']
    search_fields = ['mascota__nombre', 'diagnostico']


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'precio', 'duracion_minutos', 'is_active']
    list_filter   = ['is_active']
    search_fields = ['nombre']


class DetalleFacturaInline(admin.TabularInline):
    model  = DetalleFactura
    extra  = 0
    fields = ['servicio', 'cantidad', 'precio_unitario']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display    = ['id', 'cliente', 'total', 'pagada', 'fecha']
    list_filter     = ['pagada']
    search_fields   = ['cliente__user__username']
    inlines         = [DetalleFacturaInline]
    readonly_fields = ['total', 'fecha']
