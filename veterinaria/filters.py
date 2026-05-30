import django_filters
from veterinaria.models import Mascota, Cita, Factura


class MascotaFilter(django_filters.FilterSet):
    nombre       = django_filters.CharFilter(lookup_expr='icontains')
    especie      = django_filters.CharFilter(lookup_expr='iexact')
    cliente_nombre = django_filters.CharFilter(
        field_name='cliente__user__username', lookup_expr='icontains'
    )

    class Meta:
        model  = Mascota
        fields = ['especie', 'is_active', 'cliente']


class CitaFilter(django_filters.FilterSet):
    desde = django_filters.DateFilter(field_name='fecha', lookup_expr='gte')
    hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='lte')

    class Meta:
        model  = Cita
        fields = ['estado', 'veterinario', 'mascota']


class FacturaFilter(django_filters.FilterSet):
    desde = django_filters.DateFilter(field_name='fecha', lookup_expr='date__gte')
    hasta = django_filters.DateFilter(field_name='fecha', lookup_expr='date__lte')

    class Meta:
        model  = Factura
        fields = ['pagada', 'cliente']
