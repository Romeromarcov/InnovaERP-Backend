from django.db import models
import uuid

class Moneda(models.Model):
    id_moneda = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_iso = models.CharField(max_length=3, unique=True)  # Ej: 'USD', 'EUR', 'VES'
    nombre = models.CharField(max_length=50)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    tipo_operacion = models.CharField(max_length=50, null=True, blank=True)
    fecha_cierre_estimada = models.DateField(null=True, blank=True)
    simbolo = models.CharField(max_length=5)
    decimales = models.IntegerField(default=2)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo_iso})"

class TasaCambio(models.Model):
    id_tasa_cambio = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE)
    id_moneda_origen = models.ForeignKey(Moneda, related_name='tasa_origen', on_delete=models.CASCADE)
    id_moneda_destino = models.ForeignKey(Moneda, related_name='tasa_destino', on_delete=models.CASCADE)
    tipo_tasa = models.CharField(max_length=20, choices=[
        ('OFICIAL_BCV', 'Oficial BCV'),
        ('ESPECIAL_USUARIO', 'Especial Usuario'),
        ('PROMEDIO_MERCADO', 'Promedio Mercado'),
        ('FIJA', 'Fija')
    ])
    valor_tasa = models.DecimalField(max_digits=18, decimal_places=8)
    fecha_tasa = models.DateField()
    hora_tasa = models.TimeField(null=True, blank=True)
    id_usuario_registro = models.ForeignKey('core.Usuarios', null=True, blank=True, on_delete=models.SET_NULL)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    tipo_operacion = models.CharField(max_length=50, null=True, blank=True)
    fecha_cierre_estimada = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class MetodoPago(models.Model):
    id_metodo_pago = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    nombre_metodo = models.CharField(max_length=100)
    tipo_metodo = models.CharField(max_length=50, choices=[
        ('EFECTIVO', 'Efectivo'),
        ('ELECTRONICO', 'Electrónico'),
        ('CHEQUE', 'Cheque'),
        ('CREDITO', 'Crédito'),
        ('OTRO', 'Otro')
    ])
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class TipoImpuesto(models.Model):
    id_tipo_impuesto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    nombre_impuesto = models.CharField(max_length=100)
    codigo_impuesto = models.CharField(max_length=20, unique=True)
    es_retencion = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class ConfiguracionImpuesto(models.Model):
    id_configuracion_impuesto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    id_tipo_impuesto = models.ForeignKey(TipoImpuesto, on_delete=models.CASCADE)
    porcentaje_tasa = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio_vigencia = models.DateField()
    fecha_fin_vigencia = models.DateField(null=True, blank=True)
    es_default_venta = models.BooleanField(default=False)
    es_default_compra = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)


# MODELOS FALTANTES AGREGADOS - FINANZAS

class RetencionImpuesto(models.Model):
    id_retencion_impuesto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='retenciones_impuesto')
    id_tipo_impuesto = models.ForeignKey('TipoImpuesto', on_delete=models.CASCADE, related_name='retenciones')
    monto_base_retencion = models.DecimalField(max_digits=18, decimal_places=2)
    porcentaje_retencion = models.DecimalField(max_digits=5, decimal_places=2)
    monto_retenido = models.DecimalField(max_digits=18, decimal_places=2)
    fecha_retencion = models.DateField()
    numero_comprobante_retencion = models.CharField(max_length=100, unique=True, null=True, blank=True)
    id_documento_origen = models.UUIDField(null=True, blank=True)
    nombre_modelo_origen = models.CharField(max_length=100, null=True, blank=True)
    id_usuario_registro = models.ForeignKey('core.Usuarios', on_delete=models.CASCADE, related_name='retenciones_registradas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finanzas_retencion_impuesto'
        verbose_name = 'Retención de Impuesto'
        verbose_name_plural = 'Retenciones de Impuesto'

    def __str__(self):
        return f"Retención {self.numero_comprobante_retencion} - {self.monto_retenido}"


class TransaccionFinanciera(models.Model):
    TIPOS_TRANSACCION = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]

    id_transaccion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='transacciones_financieras')
    fecha_hora_transaccion = models.DateTimeField()
    tipo_transaccion = models.CharField(max_length=20, choices=TIPOS_TRANSACCION)
    monto_transaccion = models.DecimalField(max_digits=18, decimal_places=2)
    id_moneda_transaccion = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='transacciones_moneda')
    monto_base_empresa = models.DecimalField(max_digits=18, decimal_places=2)
    id_metodo_pago = models.ForeignKey('MetodoPago', on_delete=models.CASCADE, related_name='transacciones')
    referencia_pago = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    id_usuario_registro = models.ForeignKey('core.Usuarios', on_delete=models.CASCADE, related_name='transacciones_registradas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finanzas_transaccion_financiera'
        verbose_name = 'Transacción Financiera'
        verbose_name_plural = 'Transacciones Financieras'

    def __str__(self):
        return f"{self.tipo_transaccion} - {self.monto_transaccion}"


class Caja(models.Model):
    id_caja = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='cajas_finanzas')
    id_sucursal = models.ForeignKey('core.Sucursal', on_delete=models.CASCADE, related_name='cajas_finanzas')
    nombre_caja = models.CharField(max_length=100)
    id_moneda = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='cajas_finanzas')
    saldo_actual = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finanzas_caja'
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'

    def __str__(self):
        return f"{self.nombre_caja} - {self.saldo_actual}"


class CuentaBancariaEmpresa(models.Model):
    TIPOS_CUENTA = [
        ('AHORRO', 'Ahorro'),
        ('CORRIENTE', 'Corriente'),
        ('CREDITO', 'Crédito'),
    ]

    id_cuenta_bancaria = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='cuentas_bancarias_finanzas')
    nombre_banco = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50, unique=True)
    tipo_cuenta = models.CharField(max_length=50, choices=TIPOS_CUENTA)
    id_moneda = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='cuentas_bancarias_finanzas')
    saldo_actual = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finanzas_cuenta_bancaria_empresa'
        verbose_name = 'Cuenta Bancaria Empresa'
        verbose_name_plural = 'Cuentas Bancarias Empresa'

    def __str__(self):
        return f"{self.nombre_banco} - {self.numero_cuenta}"


class MovimientoCajaBanco(models.Model):
    TIPOS_MOVIMIENTO = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
        ('TRANSFERENCIA_ENTRADA', 'Transferencia Entrada'),
        ('TRANSFERENCIA_SALIDA', 'Transferencia Salida'),
    ]

    id_movimiento = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='movimientos_caja_banco')
    fecha_movimiento = models.DateField()
    hora_movimiento = models.TimeField()
    tipo_movimiento = models.CharField(max_length=50, choices=TIPOS_MOVIMIENTO)
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    id_moneda = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='movimientos_caja_banco')
    concepto = models.CharField(max_length=255)
    referencia = models.CharField(max_length=100, null=True, blank=True)
    id_caja = models.ForeignKey('Caja', on_delete=models.CASCADE, null=True, blank=True, related_name='movimientos')
    id_cuenta_bancaria = models.ForeignKey('CuentaBancariaEmpresa', on_delete=models.CASCADE, null=True, blank=True, related_name='movimientos')
    id_transaccion_financiera = models.ForeignKey('TransaccionFinanciera', on_delete=models.CASCADE, null=True, blank=True, related_name='movimientos_caja_banco')
    saldo_anterior = models.DecimalField(max_digits=18, decimal_places=2)
    saldo_nuevo = models.DecimalField(max_digits=18, decimal_places=2)
    id_usuario_registro = models.ForeignKey('core.Usuarios', on_delete=models.CASCADE, related_name='movimientos_caja_banco_registrados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finanzas_movimiento_caja_banco'
        verbose_name = 'Movimiento de Caja/Banco'
        verbose_name_plural = 'Movimientos de Caja/Banco'

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} ({self.fecha_movimiento})"
