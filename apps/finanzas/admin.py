from django.contrib import admin
from .models import Moneda, TasaCambio, MetodoPago, TransaccionFinanciera, Caja, CuentaBancariaEmpresa, MovimientoCajaBanco, MonedaEmpresaActiva, MetodoPagoEmpresaActiva



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
    list_display = ('nombre_metodo', 'tipo_metodo', 'empresa', 'activo', 'fecha_creacion')
    list_filter = ('tipo_metodo', 'activo', 'empresa')
    search_fields = ('nombre_metodo',)
    readonly_fields = ('id_metodo_pago', 'fecha_creacion')



@admin.register(TransaccionFinanciera)
class TransaccionFinancieraAdmin(admin.ModelAdmin):
    list_display = ['id_transaccion', 'tipo_transaccion', 'monto_transaccion', 'id_empresa', 'id_moneda_transaccion', 'id_metodo_pago', 'fecha_hora_transaccion', 'referencia_pago', 'descripcion', 'id_usuario_registro', 'fecha_creacion']
    search_fields = ['id_transaccion', 'referencia_pago', 'descripcion']

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

@admin.register(MonedaEmpresaActiva)
class MonedaEmpresaActivaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'moneda', 'activa')
    list_filter = ('empresa', 'activa')
    search_fields = ('empresa__nombre', 'moneda__nombre', 'moneda__codigo_iso')
    readonly_fields = ('id',)

@admin.register(MetodoPagoEmpresaActiva)
class MetodoPagoEmpresaActivaAdmin(admin.ModelAdmin):
    def metodo_pago_nombre(self, obj):
        return getattr(obj.metodo_pago, 'nombre_metodo', str(obj.metodo_pago))

    list_display = ('empresa', 'metodo_pago_nombre', 'activa')
    list_filter = ('empresa', 'activa')
    search_fields = ('empresa__nombre', 'metodo_pago__nombre_metodo')
    readonly_fields = ('id',)
