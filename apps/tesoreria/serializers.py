from rest_framework import serializers
from .models import Caja, MovimientoInternoFondo, OperacionCambioDivisa

class CajaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caja
        fields = '__all__'

class MovimientoInternoFondoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInternoFondo
        fields = '__all__'


class OperacionCambioDivisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperacionCambioDivisa
        fields = '__all__'
