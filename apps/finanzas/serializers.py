
from rest_framework import serializers
from .models import MetodoPagoEmpresaActiva



class MetodoPagoEmpresaActivaSerializer(serializers.ModelSerializer):
    metodo_pago = serializers.UUIDField(source='metodo_pago.id_metodo_pago')
    nombre = serializers.CharField(source='metodo_pago.nombre_metodo', read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        if request and not validated_data.get('empresa'):
            user = request.user
            empresas = getattr(user, 'empresas', None)
            if empresas and empresas.exists():
                validated_data['empresa'] = empresas.first()

        metodo_pago_value = validated_data.pop('metodo_pago', None)
        if isinstance(metodo_pago_value, dict) and 'id_metodo_pago' in metodo_pago_value:
            metodo_pago_uuid = metodo_pago_value['id_metodo_pago']
        else:
            metodo_pago_uuid = metodo_pago_value
        if metodo_pago_uuid:
            from .models import MetodoPago
            validated_data['metodo_pago'] = MetodoPago.objects.get(id_metodo_pago=metodo_pago_uuid)

        return super().create(validated_data)

    class Meta:
        model = MetodoPagoEmpresaActiva
        fields = ['id', 'empresa', 'metodo_pago', 'activa', 'nombre']
from rest_framework import serializers
from .models import (
    Moneda, TasaCambio, MetodoPago, TransaccionFinanciera, MovimientoCajaBanco, Caja,
    CuentaBancariaEmpresa, MonedaEmpresaActiva
)


class MonedaSerializer(serializers.ModelSerializer):
    pais_codigo_iso = serializers.CharField(read_only=True)
    pais_nombre = serializers.CharField(read_only=True)
    class Meta:
        model = Moneda
        fields = '__all__'
        read_only_fields = ['pais_codigo_iso', 'pais_nombre']

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

class TransaccionFinancieraSerializer(serializers.ModelSerializer):
    id_empresa_nombre = serializers.CharField(source='id_empresa.nombre_comercial', read_only=True)
    id_usuario_registro_username = serializers.CharField(source='id_usuario_registro.username', read_only=True)
    id = serializers.UUIDField(source='id_transaccion', read_only=True)
    id_moneda_transaccion__codigo_iso = serializers.CharField(source='id_moneda_transaccion.codigo_iso', read_only=True)
    id_moneda_base__codigo_iso = serializers.CharField(source='id_moneda_base.codigo_iso', read_only=True)
    id_moneda_pais_empresa__codigo_iso = serializers.CharField(source='id_moneda_pais_empresa.codigo_iso', read_only=True)
    id_metodo_pago__nombre_metodo = serializers.CharField(source='id_metodo_pago.nombre_metodo', read_only=True)
    id_usuario_registro__username = serializers.CharField(source='id_usuario_registro.username', read_only=True)
    tasa_cambio = serializers.CharField(write_only=True, required=False)
    monto_base = serializers.CharField(write_only=True, required=False)
    monto_moneda_pais = serializers.DecimalField(max_digits=18, decimal_places=2, required=False, allow_null=True)

    class Meta:
        model = TransaccionFinanciera
        fields = ['id', 'id_transaccion', 'id_empresa', 'id_empresa_nombre', 'fecha_hora_transaccion', 'tipo_transaccion', 'monto_transaccion', 'id_moneda_transaccion', 'id_moneda_base', 'id_moneda_pais_empresa', 'monto_moneda_pais', 'monto_base_empresa', 'id_metodo_pago', 'referencia_pago', 'descripcion', 'id_usuario_registro', 'id_usuario_registro_username', 'fecha_creacion', 'id_moneda_transaccion__codigo_iso', 'id_moneda_base__codigo_iso', 'id_moneda_pais_empresa__codigo_iso', 'id_metodo_pago__nombre_metodo', 'id_usuario_registro__username', 'tasa_cambio', 'monto_base']
        extra_fields = ['tasa_cambio', 'monto_base', 'id_moneda_base__codigo_iso', 'id_moneda_pais_empresa__codigo_iso', 'monto_moneda_pais']
        read_only_fields = ('id', 'id_moneda_transaccion__codigo_iso', 'id_moneda_base__codigo_iso', 'id_moneda_pais_empresa__codigo_iso', 'id_metodo_pago__nombre_metodo', 'id_usuario_registro__username')

    def create(self, validated_data):
        # Mapear monto_base del frontend a monto_base_empresa del modelo
        monto_base = validated_data.pop('monto_base', None)
        if monto_base is not None:
            validated_data['monto_base_empresa'] = monto_base
        # El campo tasa_cambio solo se usa para validación, no se guarda
        validated_data.pop('tasa_cambio', None)
        # Asignar usuario autenticado si no viene en el payload
        request = self.context.get('request')
        if request and not validated_data.get('id_usuario_registro'):
            user = request.user
            validated_data['id_usuario_registro'] = user
        # Asignar empresa si no viene en el payload y el usuario tiene empresas
        if request and not validated_data.get('id_empresa'):
            user = request.user
            empresas = getattr(user, 'empresas', None)
            if empresas and empresas.exists():
                validated_data['id_empresa'] = empresas.first()
        # Convertir id_moneda_transaccion, id_moneda_base y id_metodo_pago a instancias si vienen como UUID
        from .models import Moneda, MetodoPago, TasaCambio
        for moneda_field in ['id_moneda_transaccion', 'id_moneda_base']:
            moneda_value = validated_data.get(moneda_field)
            if isinstance(moneda_value, str):
                try:
                    validated_data[moneda_field] = Moneda.objects.get(id_moneda=moneda_value)
                except Moneda.DoesNotExist:
                    validated_data[moneda_field] = None
        metodo_value = validated_data.get('id_metodo_pago')
        if isinstance(metodo_value, str):
            validated_data['id_metodo_pago'] = MetodoPago.objects.get(id_metodo_pago=metodo_value)

        # Obtener moneda país desde la empresa
        empresa = validated_data.get('id_empresa')
        if empresa and hasattr(empresa, 'id_moneda_pais') and empresa.id_moneda_pais:
            validated_data['id_moneda_pais_empresa'] = empresa.id_moneda_pais
        else:
            validated_data['id_moneda_pais_empresa'] = None

        # Calcular monto_moneda_pais usando la tasa de cambio del día
        moneda_base = validated_data.get('id_moneda_base')
        moneda_pais = validated_data.get('id_moneda_pais_empresa')
        monto_base_empresa = validated_data.get('monto_base_empresa')
        monto_moneda_pais = None
        if moneda_base and moneda_pais and monto_base_empresa:
            from datetime import date
            hoy = date.today()
            tasa = TasaCambio.objects.filter(
                id_moneda_origen=moneda_base,
                id_moneda_destino=moneda_pais,
                fecha_tasa=hoy
            ).order_by('-fecha_tasa').first()
            if tasa:
                monto_moneda_pais = float(monto_base_empresa) * float(tasa.valor_tasa)
        validated_data['monto_moneda_pais'] = monto_moneda_pais

        return super().create(validated_data)

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
    empresa_nombre = serializers.CharField(source='empresa.nombre_comercial', read_only=True)
    moneda_codigo_iso = serializers.CharField(source='moneda.codigo_iso', read_only=True)
    moneda_nombre = serializers.CharField(source='moneda.nombre', read_only=True)
    moneda = serializers.UUIDField(source='moneda.id_moneda')
    es_base = serializers.SerializerMethodField()

    def get_es_base(self, obj):
        # Lógica: la moneda base de la empresa es la que está marcada como base en core
        # Suponiendo que Empresa tiene un campo moneda_base (ForeignKey a Moneda)
        empresa = getattr(obj, 'empresa', None)
        moneda = getattr(obj, 'moneda', None)
        if empresa and moneda:
            return getattr(empresa, 'moneda_base_id', None) == getattr(moneda, 'id_moneda', None)
        return False

    def create(self, validated_data):
        # Asignar empresa si no viene en el payload (opcional, según tu lógica)
        request = self.context.get('request')
        if request and not validated_data.get('empresa'):
            user = request.user
            empresas = getattr(user, 'empresas', None)
            if empresas and empresas.exists():
                validated_data['empresa'] = empresas.first()

        # Obtener la instancia de Moneda usando el UUID recibido
        moneda_value = validated_data.pop('moneda', None)
        if isinstance(moneda_value, dict) and 'id_moneda' in moneda_value:
            moneda_uuid = moneda_value['id_moneda']
        else:
            moneda_uuid = moneda_value
        if moneda_uuid:
            from .models import Moneda
            validated_data['moneda'] = Moneda.objects.get(id_moneda=moneda_uuid)

        return super().create(validated_data)

    class Meta:
        model = MonedaEmpresaActiva
        fields = ['id', 'empresa', 'empresa_nombre', 'moneda', 'moneda_codigo_iso', 'moneda_nombre', 'activa', 'es_base']
        read_only_fields = ['empresa', 'empresa_nombre', 'moneda_codigo_iso', 'moneda_nombre', 'es_base']
