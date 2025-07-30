from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MonedaViewSet, TasaCambioViewSet, MetodoPagoViewSet, TipoImpuestoViewSet,
    ConfiguracionImpuestoViewSet, RetencionImpuestoViewSet,
    TransaccionFinancieraViewSet, MovimientoCajaBancoViewSet, CajaViewSet,
    CuentaBancariaEmpresaViewSet, MonedaEmpresaActivaViewSet
)

router = DefaultRouter()
router.register(r'monedas', MonedaViewSet)
router.register(r'tasas-cambio', TasaCambioViewSet)
router.register(r'metodos-pago', MetodoPagoViewSet)
router.register(r'tipos-impuesto', TipoImpuestoViewSet)
router.register(r'configuracion-impuestos', ConfiguracionImpuestoViewSet)
router.register(r'retenciones-impuesto', RetencionImpuestoViewSet)
router.register(r'transacciones-financieras', TransaccionFinancieraViewSet)
router.register(r'movimientos-caja-banco', MovimientoCajaBancoViewSet)
router.register(r'cajas', CajaViewSet)
router.register(r'cuentas-bancarias-empresa', CuentaBancariaEmpresaViewSet)
router.register(r'monedas-empresa-activas', MonedaEmpresaActivaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
