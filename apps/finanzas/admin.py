from django.contrib import admin
from .models import (
    Moneda, TasaCambio, MetodoPago, TipoImpuesto, ConfiguracionImpuesto,
    RetencionImpuesto, TransaccionFinanciera, Caja, CuentaBancariaEmpresa, MovimientoCajaBanco
)


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ('codigo_iso', 'nombre', 'simbolo', 'decimales', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('codigo_iso', 'nombre')
    readonly_fields = ('id_moneda', 'fecha_creacion')


@admin.register(TasaCambio)
class TasaCambioAdmin(admin.ModelAdmin):
    list_display = ('id_moneda_origen', 'id_moneda_destino', 'tipo_tasa', 'valor_tasa', 'fecha_tasa', 'id_empresa')
    list_filter = ('tipo_tasa', 'fecha_tasa', 'id_empresa')
    search_fields = ('id_moneda_origen__codigo_iso', 'id_moneda_destino__codigo_iso')
    readonly_fields = ('id_tasa_cambio', 'fecha_creacion')


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('nombre_metodo', 'tipo_metodo', 'id_empresa', 'activo', 'fecha_creacion')
    list_filter = ('tipo_metodo', 'activo', 'id_empresa')
    search_fields = ('nombre_metodo',)
    readonly_fields = ('id_metodo_pago', 'fecha_creacion')


@admin.register(TipoImpuesto)
class TipoImpuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre_impuesto', 'codigo_impuesto', 'es_retencion', 'id_empresa', 'activo', 'fecha_creacion')
    list_filter = ('es_retencion', 'activo', 'id_empresa')
    search_fields = ('nombre_impuesto', 'codigo_impuesto')
    readonly_fields = ('id_tipo_impuesto', 'fecha_creacion')


@admin.register(ConfiguracionImpuesto)
class ConfiguracionImpuestoAdmin(admin.ModelAdmin):
    list_display = ('id_tipo_impuesto', 'porcentaje_tasa', 'fecha_inicio_vigencia', 'fecha_fin_vigencia', 'es_default_venta', 'es_default_compra', 'activo')
    list_filter = ('es_default_venta', 'es_default_compra', 'activo', 'id_empresa')
    search_fields = ('id_tipo_impuesto__nombre_impuesto',)
    readonly_fields = ('id_configuracion_impuesto',)

# Registraciones agregadas automáticamente

@admin.register(RetencionImpuesto)
class RetencionImpuestoAdmin(admin.ModelAdmin):
    list_display = ['numero_comprobante_retencion', 'monto_retenido', 'fecha_retencion']
    search_fields = ['numero_comprobante_retencion']

@admin.register(TransaccionFinanciera)
class TransaccionFinancieraAdmin(admin.ModelAdmin):
    list_display = ['tipo_transaccion', 'monto_transaccion', 'fecha_hora_transaccion']
    search_fields = ['descripcion']

@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'saldo_actual', 'activa']
    search_fields = ['nombre_caja']

@admin.register(CuentaBancariaEmpresa)
class CuentaBancariaEmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre_banco', 'numero_cuenta', 'tipo_cuenta', 'saldo_actual', 'activo']
    search_fields = ['nombre_banco', 'numero_cuenta']

@admin.register(MovimientoCajaBanco)
class MovimientoCajaBancoAdmin(admin.ModelAdmin):
    list_display = ['tipo_movimiento', 'monto', 'fecha_movimiento']
    search_fields = ['concepto', 'referencia']
