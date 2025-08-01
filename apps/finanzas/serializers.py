
from rest_framework import serializers
from .models import MetodoPagoEmpresaActiva, TipoImpuestoEmpresaActiva

class TipoImpuestoEmpresaActivaSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre_comercial', read_only=True)
    tipo_impuesto_nombre = serializers.CharField(source='tipo_impuesto.nombre_impuesto', read_only=True)
    tipo_impuesto_codigo = serializers.CharField(source='tipo_impuesto.codigo_impuesto', read_only=True)

    class Meta:
        model = TipoImpuestoEmpresaActiva
        fields = ['id', 'empresa', 'empresa_nombre', 'tipo_impuesto', 'tipo_impuesto_nombre', 'tipo_impuesto_codigo', 'activa']
        read_only_fields = ['empresa_nombre', 'tipo_impuesto_nombre', 'tipo_impuesto_codigo']

class MetodoPagoEmpresaActivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPagoEmpresaActiva
        fields = ['id', 'empresa', 'metodo_pago', 'activa']
from rest_framework import serializers
from .models import (
    Moneda, TasaCambio, MetodoPago, TipoImpuesto, ConfiguracionImpuesto,
    RetencionImpuesto, TransaccionFinanciera, MovimientoCajaBanco, Caja,
    CuentaBancariaEmpresa, MonedaEmpresaActiva, TipoImpuestoEmpresaActiva
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
    moneda_origen_nombre = serializers.CharField(source='id_moneda_origen.nombre', read_only=True)
    moneda_destino_nombre = serializers.CharField(source='id_moneda_destino.nombre', read_only=True)
    usuario_registro_username = serializers.CharField(source='id_usuario_registro.username', read_only=True)

    class Meta:
        model = TasaCambio
        fields = '__all__'
        read_only_fields = ('moneda_origen_nombre', 'moneda_destino_nombre', 'usuario_registro_username')

from rest_framework.reverse import reverse

class MetodoPagoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    aplicado = serializers.SerializerMethodField()

    class Meta:
        model = MetodoPago
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context.get('request').user if self.context.get('request') else None
        if not getattr(user, 'es_superusuario_innova', False):
            rep.pop('es_generico', None)
            rep.pop('empresa', None)
            rep.pop('es_publico', None)
        return rep

    def validate(self, data):
        user = self.context['request'].user if 'request' in self.context else None
        # Solo superusuario puede modificar métodos genéricos
        if self.instance and getattr(self.instance, 'es_generico', False) and not getattr(user, 'es_superusuario_innova', False):
            raise serializers.ValidationError('No puede modificar un método de pago genérico del sistema.')
        # Solo superusuario puede marcar como genérico o público o cambiar empresa
        if (data.get('es_generico') or data.get('es_publico') or data.get('empresa')) and not getattr(user, 'es_superusuario_innova', False):
            raise serializers.ValidationError('Solo el superusuario puede crear o modificar métodos de pago genéricos, públicos o de otra empresa.')
        # Validar unicidad de nombre_metodo por empresa y tipo_metodo si no es genérico
        es_generico = data.get('es_generico', getattr(self.instance, 'es_generico', False))
        empresa = data.get('empresa', getattr(self.instance, 'empresa', None))
        nombre_metodo = data.get('nombre_metodo', getattr(self.instance, 'nombre_metodo', None))
        tipo_metodo = data.get('tipo_metodo', getattr(self.instance, 'tipo_metodo', None))
        from .models import MetodoPago
        if not es_generico and empresa and nombre_metodo and tipo_metodo:
            qs = MetodoPago.objects.filter(nombre_metodo=nombre_metodo, es_generico=False, empresa=empresa, tipo_metodo=tipo_metodo)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'nombre_metodo': 'Ya existe un método de pago con este nombre para esta empresa y tipo.'})
        return data

    def create(self, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        # Si no es superusuario, fuerza empresa y flags
        if not getattr(user, 'es_superusuario_innova', False):
            empresas = user.empresas.all()
            validated_data['empresa'] = empresas.first() if empresas.exists() else None
            validated_data['es_generico'] = False
            validated_data['es_publico'] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        # Si no es superusuario, no puede cambiar empresa ni flags
        if not getattr(user, 'es_superusuario_innova', False):
            validated_data.pop('empresa', None)
            validated_data.pop('es_generico', None)
            validated_data.pop('es_publico', None)
        return super().update(instance, validated_data)

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('metodopago-detail', args=[obj.id_metodo_pago], request=request)

    def get_aplicado(self, obj):
        # El id_empresa_actual se pasa por context desde la view
        id_empresa_actual = self.context.get('id_empresa_actual')
        if not id_empresa_actual:
            return False
        # Buscar si existe un método similar (fuzzy) para la empresa actual usando rapidfuzz
        from .models import MetodoPago
        from rapidfuzz.fuzz import ratio
        from rapidfuzz.distance import Levenshtein
        import unicodedata
        def normalizar(s):
            s = s.lower().replace(' ', '')
            s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
            return s
        nombre_actual = normalizar(obj.nombre_metodo)
        metodos_empresa = MetodoPago.objects.filter(
            empresa=id_empresa_actual,
            tipo_metodo=obj.tipo_metodo
        )
        for mp in metodos_empresa:
            nombre_db = normalizar(mp.nombre_metodo)
            sim = ratio(nombre_actual, nombre_db)
            dist = Levenshtein.distance(nombre_actual, nombre_db)
            if (
                sim >= 55 or
                dist <= 3 or
                nombre_actual in nombre_db or
                nombre_db in nombre_actual
            ):
                return True
        return False

class TipoImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoImpuesto
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context.get('request').user if self.context.get('request') else None
        if not getattr(user, 'es_superusuario_innova', False):
            rep.pop('es_generico', None)
            rep.pop('empresa', None)
            rep.pop('es_publico', None)
        return rep

    def validate(self, data):
        user = self.context['request'].user if 'request' in self.context else None
        # Solo superusuario puede modificar tipos genéricos
        if self.instance and getattr(self.instance, 'es_generico', False) and not getattr(user, 'es_superusuario_innova', False):
            raise serializers.ValidationError('No puede modificar un tipo de impuesto genérico del sistema.')
        # Solo superusuario puede marcar como genérico o público o cambiar empresa
        if (data.get('es_generico') or data.get('es_publico') or data.get('empresa')) and not getattr(user, 'es_superusuario_innova', False):
            raise serializers.ValidationError('Solo el superusuario puede crear o modificar tipos de impuesto genéricos, públicos o de otra empresa.')
        # Validar unicidad de codigo_impuesto por empresa si no es genérico
        es_generico = data.get('es_generico', getattr(self.instance, 'es_generico', False))
        empresa = data.get('empresa', getattr(self.instance, 'empresa', None))
        codigo_impuesto = data.get('codigo_impuesto', getattr(self.instance, 'codigo_impuesto', None))
        if not es_generico:
            qs = TipoImpuesto.objects.filter(codigo_impuesto=codigo_impuesto, es_generico=False, empresa=empresa)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({'codigo_impuesto': 'Ya existe un tipo de impuesto con este código para esta empresa.'})
        return data

    def create(self, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        # Si no es superusuario, fuerza empresa y flags
        if not getattr(user, 'es_superusuario_innova', False):
            empresas = user.empresas.all()
            validated_data['empresa'] = empresas.first() if empresas.exists() else None
            validated_data['es_generico'] = False
            validated_data['es_publico'] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        # Si no es superusuario, no puede cambiar empresa ni flags
        if not getattr(user, 'es_superusuario_innova', False):
            validated_data.pop('empresa', None)
            validated_data.pop('es_generico', None)
            validated_data.pop('es_publico', None)
        return super().update(instance, validated_data)

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
    empresa_nombre = serializers.CharField(source='empresa.nombre_comercial', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    moneda_codigo_iso = serializers.CharField(source='moneda.codigo_iso', read_only=True)
    tipo_caja_display = serializers.CharField(source='get_tipo_caja_display', read_only=True)

    class Meta:
        model = Caja
        fields = '__all__'
        read_only_fields = ['empresa_nombre', 'sucursal_nombre', 'moneda_codigo_iso', 'tipo_caja_display']


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
