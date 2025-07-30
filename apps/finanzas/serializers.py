from rest_framework import serializers
from .models import (
    Moneda, TasaCambio, MetodoPago, TipoImpuesto, ConfiguracionImpuesto,
    RetencionImpuesto, TransaccionFinanciera, MovimientoCajaBanco, Caja,
    CuentaBancariaEmpresa, MonedaEmpresaActiva
)


class MonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = '__all__'
        read_only_fields = []

    def to_representation(self, instance):
        # Oculta campos sensibles para usuarios normales
        rep = super().to_representation(instance)
        user = self.context.get('request').user if self.context.get('request') else None
        if not getattr(user, 'es_superusuario_innova', False):
            rep.pop('es_generica', None)
            rep.pop('empresa', None)
        return rep

    def validate(self, data):
        user = self.context['request'].user if 'request' in self.context else None
        tipo_moneda = data.get('tipo_moneda', getattr(self.instance, 'tipo_moneda', None))
        codigo_iso = data.get('codigo_iso', getattr(self.instance, 'codigo_iso', None))
        # Validación de código ISO
        if tipo_moneda == 'crypto':
            if not (4 <= len(codigo_iso) <= 5):
                raise serializers.ValidationError({
                    'codigo_iso': 'Para monedas cripto, el código ISO debe tener 4 o 5 caracteres.'
                })
        else:
            if len(codigo_iso) > 3:
                raise serializers.ValidationError({
                    'codigo_iso': 'Para monedas fiat u otro, el código ISO debe tener máximo 3 caracteres.'
                })
        # Solo superusuario puede modificar monedas genéricas
        if self.instance and self.instance.es_generica and not getattr(user, 'es_superusuario_innova', False):
            raise serializers.ValidationError('No puede modificar una moneda genérica del sistema.')
        # Solo superusuario puede marcar como genérica o pública o cambiar empresa
        if (data.get('es_generica') or data.get('es_publica') or data.get('empresa')) and not getattr(user, 'es_superusuario_innova', False):
            raise serializers.ValidationError('Solo el superusuario puede crear o modificar monedas genéricas, públicas o de otra empresa.')

        # Validar unicidad de codigo_iso por empresa si no es genérica
        es_generica = data.get('es_generica', getattr(self.instance, 'es_generica', False))
        empresa = data.get('empresa', getattr(self.instance, 'empresa', None))
        if not es_generica:
            qs = Moneda.objects.filter(codigo_iso=codigo_iso, es_generica=False, empresa=empresa)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'codigo_iso': 'Ya existe una moneda con este código ISO para esta empresa.'})
        return data

    def create(self, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        # Si no es superusuario, fuerza empresa y flags
        if not getattr(user, 'es_superusuario_innova', False):
            empresas = user.empresas.all()
            validated_data['empresa'] = empresas.first() if empresas.exists() else None
            validated_data['es_generica'] = False
            validated_data['es_publica'] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        # Si no es superusuario, no puede cambiar empresa ni flags
        if not getattr(user, 'es_superusuario_innova', False):
            validated_data.pop('empresa', None)
            validated_data.pop('es_generica', None)
            validated_data.pop('es_publica', None)
        return super().update(instance, validated_data)

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


class MonedaEmpresaActivaSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and not validated_data.get('empresa'):
            user = request.user
            empresas = getattr(user, 'empresas', None)
            if empresas and empresas.exists():
                validated_data['empresa'] = empresas.first()
        return super().create(validated_data)
    empresa_nombre = serializers.CharField(source='empresa.nombre_comercial', read_only=True)
    moneda_codigo_iso = serializers.CharField(source='moneda.codigo_iso', read_only=True)
    moneda_nombre = serializers.CharField(source='moneda.nombre', read_only=True)

    class Meta:
        model = MonedaEmpresaActiva
        fields = ['id', 'empresa', 'empresa_nombre', 'moneda', 'moneda_codigo_iso', 'moneda_nombre', 'activa']
        read_only_fields = ['empresa', 'empresa_nombre', 'moneda_codigo_iso', 'moneda_nombre']
