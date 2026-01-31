
from rest_framework import permissions
from apps.core.viewsets import BaseModelViewSet
from .models import MetodoPagoEmpresaActiva
from .serializers import MetodoPagoEmpresaActivaSerializer
# ViewSet para MetodoPagoEmpresaActiva
from rest_framework import viewsets, permissions

class MetodoPagoEmpresaActivaViewSet(viewsets.ModelViewSet):
    queryset = MetodoPagoEmpresaActiva.objects.all()
    serializer_class = MetodoPagoEmpresaActivaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        empresa = self.request.query_params.get('empresa')
        metodo_pago = self.request.query_params.get('metodo_pago')
        if empresa:
            qs = qs.filter(empresa=empresa)
        if metodo_pago:
            qs = qs.filter(metodo_pago=metodo_pago)
        return qs
from rest_framework import viewsets
from django.db import models
from .models import (
    Moneda, TasaCambio, MetodoPago, TransaccionFinanciera, MovimientoCajaBanco, Caja,
    CuentaBancariaEmpresa, MonedaEmpresaActiva
)
from .serializers import (
    MonedaSerializer, TasaCambioSerializer, MetodoPagoSerializer,
    TransaccionFinancieraSerializer,
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

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.core.models import Empresa

class MetodoPagoViewSet(BaseModelViewSet):

    def get_object(self):
        # Permitir reutilizar métodos de pago de cualquier empresa
        if hasattr(self, 'action') and self.action == 'reutilizar':
            return MetodoPago.objects.get(id_metodo_pago=self.kwargs[self.lookup_field])
        return super().get_object()

    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    lookup_field = 'id_metodo_pago'
    lookup_value_regex = '[0-9a-f-]{36}'

    def get_queryset(self):
        """
        Por defecto, filtra por empresa actual salvo que sea superusuario InnovaERP.
        Incluye métodos genéricos, públicos y de la(s) empresa(s) del usuario.
        """
        user = self.request.user
        if getattr(user, 'es_superusuario_innova', False):
            return MetodoPago.objects.all()
        empresas_usuario = user.empresas.all()
        metodos_visibles = MetodoPago.objects.filter(
            models.Q(es_generico=True)
            | models.Q(es_publico=True)
            | models.Q(empresa__in=empresas_usuario)
        ).distinct()
        return metodos_visibles

    @action(detail=False, methods=['get'], url_path='buscar_reutilizar')
    def buscar_reutilizar(self, request):
        """
        Devuelve métodos de pago reutilizables (de otras empresas, genéricos o públicos) para la empresa actual.
        Marca con 'aplicado' los que ya están en la empresa actual (por nombre y tipo).
        """
        id_empresa_actual = request.query_params.get('id_empresa_actual')
        empresas_excluir = []
        if id_empresa_actual:
            empresas_excluir.append(id_empresa_actual)
        queryset = MetodoPago.objects.filter(
            models.Q(es_generico=True)
            | models.Q(es_publico=True)
            | (~models.Q(empresa__in=empresas_excluir) & ~models.Q(empresa=None))
        )
        if id_empresa_actual:
            queryset = queryset.exclude(empresa=id_empresa_actual)
        nombre_metodo = request.query_params.get('nombre_metodo')
        tipo_metodo = request.query_params.get('tipo_metodo')
        if nombre_metodo:
            queryset = queryset.filter(nombre_metodo__icontains=nombre_metodo)
        if tipo_metodo:
            queryset = queryset.filter(tipo_metodo=tipo_metodo)
        page = self.paginate_queryset(queryset)
        serializer_context = self.get_serializer_context()
        serializer_context['id_empresa_actual'] = id_empresa_actual
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=serializer_context)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='reutilizar')
    def reutilizar(self, request, *args, **kwargs):
        """
        Asocia el método de pago existente a la empresa indicada (sin copiar, solo crea la relación).
        Si ya existe para esa empresa, retorna error.
        """
        metodo = self.get_object()
        id_empresa = request.data.get('id_empresa')
        if not id_empresa:
            return Response({'detail': 'id_empresa es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            empresa = Empresa.objects.get(id_empresa=id_empresa)
        except Empresa.DoesNotExist:
            return Response({'detail': 'Empresa no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        # Validación fuzzy robusta: rapidfuzz ratio, distancia Levenshtein, substring y normalización de acentos
        from rapidfuzz.fuzz import ratio
        from rapidfuzz.distance import Levenshtein
        import unicodedata
        def normalizar(s):
            s = s.lower().replace(' ', '')
            s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
            return s
        nombre_actual = normalizar(metodo.nombre_metodo)
        metodos_existentes = MetodoPago.objects.filter(
            empresa=empresa,
            tipo_metodo=metodo.tipo_metodo
        )
        for mp in metodos_existentes:
            nombre_db = normalizar(mp.nombre_metodo)
            sim = ratio(nombre_actual, nombre_db)
            dist = Levenshtein.distance(nombre_actual, nombre_db)
            if (
                sim >= 55 or
                dist <= 3 or
                nombre_actual in nombre_db or
                nombre_db in nombre_actual
            ):
                return Response({'detail': f"Ya existe un método de pago similar ('{mp.nombre_metodo}') para esta empresa."}, status=status.HTTP_409_CONFLICT)
        # Asociar (crear nuevo registro con los mismos datos, pero empresa diferente)
        nuevo = MetodoPago.objects.create(
            empresa=empresa,
            nombre_metodo=metodo.nombre_metodo,
            tipo_metodo=metodo.tipo_metodo,
            activo=True,
            referencia_externa=metodo.referencia_externa,
            documento_json=metodo.documento_json,
            es_generico=False,
            es_publico=False
        )
        serializer = self.get_serializer(nuevo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TransaccionFinancieraViewSet(BaseModelViewSet):
    queryset = TransaccionFinanciera.objects.all()
    serializer_class = TransaccionFinancieraSerializer

    def perform_create(self, serializer):
        # El serializer ya crea el MovimientoCajaBanco automáticamente
        serializer.save()


    def get_queryset(self):
        user = self.request.user
        # Superusuario ve todas
        if getattr(user, 'es_superusuario_innova', False):
            return TransaccionFinanciera.objects.all()
        empresas_usuario = user.empresas.all()
        # Filtrar por empresa si se pasa id_empresa como query param
        id_empresa = self.request.query_params.get('id_empresa')
        qs = TransaccionFinanciera.objects.all()
        if id_empresa:
            qs = qs.filter(empresa_id=id_empresa)
        elif empresas_usuario.exists():
            qs = qs.filter(empresa_id__in=empresas_usuario.values_list('id_empresa', flat=True))
        return qs


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
