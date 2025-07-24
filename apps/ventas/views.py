
from rest_framework import viewsets
from .models import (
    Pedido, DetallePedido, NotaVenta, DetalleNotaVenta, Factura,
    DetalleFactura, NotaCreditoVenta, DetalleNotaCreditoVenta,
    DevolucionVenta, DetalleDevolucionVenta, Cotizacion, DetalleCotizacion
)
from .serializers import (
    PedidoSerializer, DetallePedidoSerializer, NotaVentaSerializer,
    DetalleNotaVentaSerializer, FacturaSerializer, DetalleFacturaSerializer,
    NotaCreditoVentaSerializer, DetalleNotaCreditoVentaSerializer,
    DevolucionVentaSerializer, DetalleDevolucionVentaSerializer,
    CotizacionSerializer, DetalleCotizacionSerializer
)
from rest_framework.permissions import IsAuthenticated
from apps.core.viewsets import BaseModelViewSet

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [IsAuthenticated]

class NotaVentaViewSet(viewsets.ModelViewSet):
    queryset = NotaVenta.objects.all()
    serializer_class = NotaVentaSerializer
    permission_classes = [IsAuthenticated]

class DetalleNotaVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleNotaVenta.objects.all()
    serializer_class = DetalleNotaVentaSerializer
    permission_classes = [IsAuthenticated]


class FacturaViewSet(BaseModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer


class DetalleFacturaViewSet(BaseModelViewSet):
    queryset = DetalleFactura.objects.all()
    serializer_class = DetalleFacturaSerializer


class NotaCreditoVentaViewSet(BaseModelViewSet):
    queryset = NotaCreditoVenta.objects.all()
    serializer_class = NotaCreditoVentaSerializer


class DetalleNotaCreditoVentaViewSet(BaseModelViewSet):
    queryset = DetalleNotaCreditoVenta.objects.all()
    serializer_class = DetalleNotaCreditoVentaSerializer


class DevolucionVentaViewSet(BaseModelViewSet):
    queryset = DevolucionVenta.objects.all()
    serializer_class = DevolucionVentaSerializer


class DetalleDevolucionVentaViewSet(BaseModelViewSet):
    queryset = DetalleDevolucionVenta.objects.all()
    serializer_class = DetalleDevolucionVentaSerializer


class CotizacionViewSet(BaseModelViewSet):
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer


class DetalleCotizacionViewSet(BaseModelViewSet):
    queryset = DetalleCotizacion.objects.all()
    serializer_class = DetalleCotizacionSerializer
