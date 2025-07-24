from rest_framework import serializers
from .models import (
    Pedido, DetallePedido, NotaVenta, DetalleNotaVenta, Factura,
    DetalleFactura, NotaCreditoVenta, DetalleNotaCreditoVenta,
    DevolucionVenta, DetalleDevolucionVenta, Cotizacion, DetalleCotizacion
)

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

    def validate_numero_pedido(self, value):
        if not value:
            raise serializers.ValidationError("El número de pedido es obligatorio.")
        return value

    def validate(self, data):
        if data.get('fecha_cierre_estimada') and data['fecha_cierre_estimada'] < data['fecha_pedido']:
            raise serializers.ValidationError({
                'fecha_cierre_estimada': "La fecha de cierre estimada no puede ser anterior a la fecha del pedido."
            })
        return data

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero.")
        return value

    def validate_precio_unitario(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo.")
        return value


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'


class DetalleFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleFactura
        fields = '__all__'


class NotaCreditoVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaCreditoVenta
        fields = '__all__'


class DetalleNotaCreditoVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleNotaCreditoVenta
        fields = '__all__'


class DevolucionVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevolucionVenta
        fields = '__all__'


class DetalleDevolucionVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleDevolucionVenta
        fields = '__all__'


class CotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizacion
        fields = '__all__'


class DetalleCotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCotizacion
        fields = '__all__'

class NotaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaVenta
        fields = '__all__'

    def validate_numero_nota(self, value):
        if not value:
            raise serializers.ValidationError("El número de nota es obligatorio.")
        return value

class DetalleNotaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleNotaVenta
        fields = '__all__'

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero.")
        return value

    def validate_precio_unitario(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo.")
        return value
