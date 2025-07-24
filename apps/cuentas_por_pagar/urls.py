from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CuentaPorPagarViewSet, PagoCxPViewSet

router = DefaultRouter()
router.register(r'cuentas-por-pagar', CuentaPorPagarViewSet)
router.register(r'pagos-cxp', PagoCxPViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
