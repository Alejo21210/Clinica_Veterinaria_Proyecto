from rest_framework import serializers
from veterinaria.models import Cliente, Factura, DetalleFactura, Servicio
from veterinaria.serializers.servicio import ServicioSerializer


class DetalleFacturaSerializer(serializers.ModelSerializer):
    servicio = ServicioSerializer(read_only=True)
    servicio_id = serializers.PrimaryKeyRelatedField(
        source='servicio',
        write_only=True,
        queryset=Servicio.objects.none(),
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model  = DetalleFactura
        fields = ['id', 'servicio', 'servicio_id', 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = ['id', 'precio_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio_id'].queryset = Servicio.objects.filter(is_active=True)

    def get_subtotal(self, obj):
        return obj.subtotal


class FacturaSerializer(serializers.ModelSerializer):
    detalles         = DetalleFacturaSerializer(many=True, read_only=True)
    cliente          = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(), required=False,
    )
    cliente_nombre   = serializers.CharField(source='cliente.user.username', read_only=True)
    num_servicios    = serializers.SerializerMethodField()

    class Meta:
        model  = Factura
        fields = [
            'id', 'cliente', 'cliente_nombre',
            'detalles', 'num_servicios',
            'total', 'pagada', 'fecha', 'created_at',
        ]
        read_only_fields = ['id', 'total', 'fecha', 'created_at']

    def get_num_servicios(self, obj):
        return obj.detalles.count()
