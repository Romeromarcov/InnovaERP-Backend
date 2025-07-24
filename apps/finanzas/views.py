from rest_framework import viewsets
from .models import (
    Moneda, TasaCambio, MetodoPago, TipoImpuesto, ConfiguracionImpuesto,
    RetencionImpuesto, TransaccionFinanciera, MovimientoCajaBanco, Caja,
    CuentaBancariaEmpresa
)
from .serializers import (
    MonedaSerializer, TasaCambioSerializer, MetodoPagoSerializer,
    TipoImpuestoSerializer, ConfiguracionImpuestoSerializer,
    RetencionImpuestoSerializer, TransaccionFinancieraSerializer,
    MovimientoCajaBancoSerializer, CajaSerializer, CuentaBancariaEmpresaSerializer
)
from apps.core.viewsets import BaseModelViewSet

class MonedaViewSet(BaseModelViewSet):
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializer

class TasaCambioViewSet(BaseModelViewSet):
    queryset = TasaCambio.objects.all()
    serializer_class = TasaCambioSerializer

class MetodoPagoViewSet(BaseModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class TipoImpuestoViewSet(BaseModelViewSet):
    queryset = TipoImpuesto.objects.all()
    serializer_class = TipoImpuestoSerializer

class ConfiguracionImpuestoViewSet(BaseModelViewSet):
    queryset = ConfiguracionImpuesto.objects.all()
    serializer_class = ConfiguracionImpuestoSerializer


class RetencionImpuestoViewSet(BaseModelViewSet):
    queryset = RetencionImpuesto.objects.all()
    serializer_class = RetencionImpuestoSerializer


class TransaccionFinancieraViewSet(BaseModelViewSet):
    queryset = TransaccionFinanciera.objects.all()
    serializer_class = TransaccionFinancieraSerializer


class MovimientoCajaBancoViewSet(BaseModelViewSet):
    queryset = MovimientoCajaBanco.objects.all()
    serializer_class = MovimientoCajaBancoSerializer


class CajaViewSet(BaseModelViewSet):
    queryset = Caja.objects.all()
    serializer_class = CajaSerializer


class CuentaBancariaEmpresaViewSet(BaseModelViewSet):
    queryset = CuentaBancariaEmpresa.objects.all()
    serializer_class = CuentaBancariaEmpresaSerializer
