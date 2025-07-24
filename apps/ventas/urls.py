from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PedidoViewSet, DetallePedidoViewSet, NotaVentaViewSet,
    DetalleNotaVentaViewSet, FacturaViewSet, DetalleFacturaViewSet,
    NotaCreditoVentaViewSet, DetalleNotaCreditoVentaViewSet,
    DevolucionVentaViewSet, DetalleDevolucionVentaViewSet, CotizacionViewSet,
    DetalleCotizacionViewSet
)

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'notas-venta', NotaVentaViewSet)
router.register(r'detalles-nota-venta', DetalleNotaVentaViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'detalles-factura', DetalleFacturaViewSet)
router.register(r'notas-credito-venta', NotaCreditoVentaViewSet)
router.register(r'detalles-nota-credito-venta', DetalleNotaCreditoVentaViewSet)
router.register(r'devoluciones-venta', DevolucionVentaViewSet)
router.register(r'detalles-devolucion-venta', DetalleDevolucionVentaViewSet)
router.register(r'cotizaciones', CotizacionViewSet)
router.register(r'detalles-cotizacion', DetalleCotizacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
