from rest_framework import serializers
from .models import CuentaPorPagar, PagoCxP

class CuentaPorPagarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuentaPorPagar
        fields = '__all__'

class PagoCxPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoCxP
        fields = '__all__'
