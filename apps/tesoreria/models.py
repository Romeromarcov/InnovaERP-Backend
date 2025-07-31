from django.db import models

from apps.core.models import Empresa
from apps.finanzas.models import Moneda, Caja

class MovimientoInternoFondo(models.Model):
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    caja_origen = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='movimientos_salida')
    caja_destino = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='movimientos_entrada')
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.caja_origen} -> {self.caja_destino}: {self.monto}"


class OperacionCambioDivisa(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='operaciones_cambio')
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    numero_operacion = models.CharField(max_length=50, unique=True)
    fecha_operacion = models.DateTimeField()
    tipo_operacion = models.CharField(max_length=20, choices=[
        ('COMPRA', 'Compra'),
        ('VENTA', 'Venta')
    ])
    moneda_origen = models.ForeignKey('finanzas.Moneda', on_delete=models.CASCADE, related_name='operaciones_origen')
    moneda_destino = models.ForeignKey('finanzas.Moneda', on_delete=models.CASCADE, related_name='operaciones_destino')
    monto_origen = models.DecimalField(max_digits=18, decimal_places=4)
    tasa_cambio = models.DecimalField(max_digits=18, decimal_places=6)
    monto_destino = models.DecimalField(max_digits=18, decimal_places=4)
    comision = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    observaciones = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tesoreria_operacion_cambio_divisa'
        verbose_name = 'Operación de Cambio de Divisa'
        verbose_name_plural = 'Operaciones de Cambio de Divisa'

    def __str__(self):
        return f"{self.numero_operacion} - {self.tipo_operacion}: {self.monto_origen} {self.moneda_origen} -> {self.monto_destino} {self.moneda_destino}"
