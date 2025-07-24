from rest_framework import serializers
from .models import (
    Moneda, TasaCambio, MetodoPago, TipoImpuesto, ConfiguracionImpuesto,
    RetencionImpuesto, TransaccionFinanciera, MovimientoCajaBanco, Caja,
    CuentaBancariaEmpresa
)

class MonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = '__all__'

class TasaCambioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasaCambio
        fields = '__all__'

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class TipoImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoImpuesto
        fields = '__all__'

class ConfiguracionImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionImpuesto
        fields = '__all__'


class RetencionImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetencionImpuesto
        fields = '__all__'


class TransaccionFinancieraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaccionFinanciera
        fields = '__all__'


class MovimientoCajaBancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCajaBanco
        fields = '__all__'


class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'


class CuentaBancariaEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaBancariaEmpresa
        fields = '__all__'
