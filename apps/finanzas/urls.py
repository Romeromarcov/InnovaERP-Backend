from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_extra.tasa_oficial_bcv import TasaCambioOficialBCVView
from .views import MonedaViewSet, TasaCambioViewSet, MetodoPagoViewSet, \
    TransaccionFinancieraViewSet, \
    MovimientoCajaBancoViewSet, CajaViewSet, CuentaBancariaEmpresaViewSet, MonedaEmpresaActivaViewSet, MetodoPagoEmpresaActivaViewSet
from .views_ajustes import AjusteCajaBancoViewSet

router = DefaultRouter()
router.register(r'monedas', MonedaViewSet)
router.register(r'tasas-cambio', TasaCambioViewSet)
router.register(r'metodos-pago', MetodoPagoViewSet)
router.register(r'transacciones-financieras', TransaccionFinancieraViewSet)
router.register(r'movimientos-caja-banco', MovimientoCajaBancoViewSet)
router.register(r'cajas', CajaViewSet)
router.register(r'cuentas-bancarias-empresa', CuentaBancariaEmpresaViewSet)
router.register(r'monedas-empresa-activas', MonedaEmpresaActivaViewSet)
router.register(r'metodos-pago-empresa-activas', MetodoPagoEmpresaActivaViewSet, basename='metodos-pago-empresa-activas')
router.register(r'ajustes-caja-banco', AjusteCajaBancoViewSet, basename='ajustes-caja-banco')



urlpatterns = [
    path('', include(router.urls)),
    path('tasa-oficial-bcv/', TasaCambioOficialBCVView.as_view(), name='tasa-oficial-bcv'),
]
