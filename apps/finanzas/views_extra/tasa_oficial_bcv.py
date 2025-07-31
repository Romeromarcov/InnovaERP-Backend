from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.finanzas.models import TasaCambio, Moneda
from apps.finanzas.serializers import TasaCambioSerializer
from datetime import date

class TasaCambioOficialBCVView(APIView):
    """
    Devuelve la tasa oficial BCV global (id_empresa=None) para la fecha actual o la fecha indicada.
    Parámetros GET opcionales:
      - fecha (YYYY-MM-DD)
      - moneda_origen (ej: USD)
      - moneda_destino (ej: VES)
    """
    def get(self, request):
        fecha = request.GET.get('fecha', date.today())
        if isinstance(fecha, str):
            try:
                fecha = date.fromisoformat(fecha)
            except Exception:
                return Response({'detail': 'Formato de fecha inválido. Use YYYY-MM-DD.'}, status=400)
        moneda_origen = request.GET.get('moneda_origen', 'USD')
        moneda_destino = request.GET.get('moneda_destino', 'VES')
        try:
            origen = Moneda.objects.get(codigo_iso=moneda_origen)
            destino = Moneda.objects.get(codigo_iso=moneda_destino)
        except Moneda.DoesNotExist:
            return Response({'detail': 'Moneda no encontrada.'}, status=404)
        tasa = TasaCambio.objects.filter(
            fecha_tasa=fecha,
            id_moneda_origen=origen,
            id_moneda_destino=destino,
            tipo_tasa='OFICIAL_BCV',
            id_empresa=None
        ).order_by('-fecha_tasa').first()
        if not tasa:
            return Response({'detail': 'No hay tasa oficial BCV registrada para esa fecha.'}, status=404)
        return Response(TasaCambioSerializer(tasa).data)
