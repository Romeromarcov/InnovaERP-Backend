from rest_framework import viewsets
from django.db import models
from .models import (
    Moneda, TasaCambio, MetodoPago, TipoImpuesto, ConfiguracionImpuesto,
    RetencionImpuesto, TransaccionFinanciera, MovimientoCajaBanco, Caja,
    CuentaBancariaEmpresa, MonedaEmpresaActiva
)
from .serializers import (
    MonedaSerializer, TasaCambioSerializer, MetodoPagoSerializer,
    TipoImpuestoSerializer, ConfiguracionImpuestoSerializer,
    RetencionImpuestoSerializer, TransaccionFinancieraSerializer,
    MovimientoCajaBancoSerializer, CajaSerializer, CuentaBancariaEmpresaSerializer,
    MonedaEmpresaActivaSerializer
)
from apps.core.viewsets import BaseModelViewSet
from rest_framework import permissions

class MonedaViewSet(BaseModelViewSet):
    from rest_framework.decorators import action
    from rest_framework.response import Response

    @action(detail=False, methods=['get'], url_path='activas')
    def activas(self, request):
        user = request.user
        if getattr(user, 'es_superusuario_innova', False):
            queryset = Moneda.objects.all()
        else:
            empresas_usuario = user.empresas.all()
            monedas_visibles = Moneda.objects.filter(
                models.Q(es_generica=True)
                | models.Q(es_publica=True)
                | models.Q(empresa__in=empresas_usuario)
            ).distinct()
            if not empresas_usuario.exists():
                queryset = monedas_visibles
            else:
                empresa = empresas_usuario.first()
                activas_ids = set(
                    MonedaEmpresaActiva.objects.filter(empresa=empresa, activa=True).values_list('moneda_id', flat=True)
                )
                queryset = monedas_visibles.filter(id_moneda__in=activas_ids)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializer

    def get_queryset(self):
        user = self.request.user
        # Superusuario InnovaERP ve todas
        if getattr(user, 'es_superusuario_innova', False):
            return Moneda.objects.all()
        empresas_usuario = user.empresas.all()
        # Monedas visibles (genéricas, públicas, propias)
        monedas_visibles = Moneda.objects.filter(
            models.Q(es_generica=True)
            | models.Q(es_publica=True)
            | models.Q(empresa__in=empresas_usuario)
        ).distinct()
        return monedas_visibles

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


class MonedaEmpresaActivaViewSet(BaseModelViewSet):

    queryset = MonedaEmpresaActiva.objects.all()
    serializer_class = MonedaEmpresaActivaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'es_superusuario_innova', False):
            return MonedaEmpresaActiva.objects.all()
        empresas = user.empresas.all()
        return MonedaEmpresaActiva.objects.filter(empresa__in=empresas)
