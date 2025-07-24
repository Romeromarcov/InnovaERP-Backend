from django.contrib import admin
from .models import (
    Pedido,
    DetallePedido,
    NotaVenta,
    DetalleNotaVenta,
    Factura,
    Cotizacion,
    DetalleCotizacion,
    DetalleFactura,
    NotaCreditoVenta,
    DetalleNotaCreditoVenta,
    DevolucionVenta,
    DetalleDevolucionVenta
)

# Register your models here.
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(NotaVenta)
admin.site.register(DetalleNotaVenta)
admin.site.register(Factura)

# Registraciones agregadas automáticamente

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']

@admin.register(DetalleCotizacion)
class DetalleCotizacionAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']

@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']

@admin.register(NotaCreditoVenta)
class NotaCreditoVentaAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']

@admin.register(DetalleNotaCreditoVenta)
class DetalleNotaCreditoVentaAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']

@admin.register(DevolucionVenta)
class DevolucionVentaAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']

@admin.register(DetalleDevolucionVenta)
class DetalleDevolucionVentaAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']
