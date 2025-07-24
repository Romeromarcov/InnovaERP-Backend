
from rest_framework import viewsets
from .models import CuentaPorPagar, PagoCxP
from .serializers import CuentaPorPagarSerializer, PagoCxPSerializer
from apps.core.viewsets import BaseModelViewSet

class CuentaPorPagarViewSet(BaseModelViewSet):
    queryset = CuentaPorPagar.objects.all()
    serializer_class = CuentaPorPagarSerializer

class PagoCxPViewSet(BaseModelViewSet):
    queryset = PagoCxP.objects.all()
    serializer_class = PagoCxPSerializer
