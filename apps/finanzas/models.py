
import uuid
from django.db import models

class Moneda(models.Model):
    id_moneda = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TIPO_MONEDA_CHOICES = [
        ('fiat', 'Fiat'),
        ('crypto', 'Cripto'),
        ('otro', 'Otro'),
    ]
    tipo_moneda = models.CharField(max_length=10, choices=TIPO_MONEDA_CHOICES, default='fiat')
    codigo_iso = models.CharField(max_length=5, unique=True)  # Ej: 'USD', 'EUR', 'VES', 'USDT', 'WBTC'
    nombre = models.CharField(max_length=50)
    pais_codigo_iso = models.CharField(max_length=3, null=True, blank=True, verbose_name="Código ISO del País")
    pais_nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre del País")
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    tipo_operacion = models.CharField(max_length=50, null=True, blank=True)
    fecha_cierre_estimada = models.DateField(null=True, blank=True)
    simbolo = models.CharField(max_length=5)
    decimales = models.IntegerField(default=2)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    es_generica = models.BooleanField(default=False, help_text="Si es True, es una moneda global del sistema, no editable por usuarios normales.")
    es_publica = models.BooleanField(default=False, help_text="Si es True, la moneda es visible para todas las empresas.")
    empresa = models.ForeignKey('core.Empresa', null=True, blank=True, on_delete=models.CASCADE, related_name='monedas_empresa', help_text="Empresa propietaria de la moneda. Null si es genérica.")
    def __str__(self):
        return f"{self.nombre} ({self.codigo_iso})"

# Modelo para métodos de pago activos por empresa
class MetodoPagoEmpresaActiva(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='metodos_pago_activos')
    metodo_pago = models.ForeignKey('MetodoPago', on_delete=models.CASCADE, related_name='empresas_activas')
    activa = models.BooleanField(default=True)

# Modelo para monedas activas por empresa
class MonedaEmpresaActiva(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='monedas_activas')
    moneda = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='empresas_activas')
    activa = models.BooleanField(default=True)


class TasaCambio(models.Model):
    id_tasa_cambio = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, null=True, blank=True, help_text="Para OFICIAL_BCV puede ser null y será global para todas las empresas.")
    id_moneda_origen = models.ForeignKey('Moneda', related_name='tasa_origen', on_delete=models.CASCADE)
    id_moneda_destino = models.ForeignKey('Moneda', related_name='tasa_destino', on_delete=models.CASCADE)
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
    empresa = models.ForeignKey('core.Empresa', null=True, blank=True, on_delete=models.CASCADE, related_name='metodos_pago_empresa', help_text="Empresa propietaria del método. Null si es genérico.")
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    nombre_metodo = models.CharField(max_length=100)
    tipo_metodo = models.CharField(max_length=50, choices=[
        ('EFECTIVO', 'Efectivo'),
        ('ELECTRONICO', 'Electrónico'),
        ('TARJETA', 'Tarjeta'),
        ('CHEQUE', 'Cheque'),
        ('CREDITO', 'Crédito'),
        ('OTRO', 'Otro')
    ])
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # NUEVOS CAMPOS PARA MULTI-TENANT Y VISIBILIDAD
    es_generico = models.BooleanField(default=False, help_text="Si es True, es un método global del sistema, no editable por usuarios normales.")
    es_publico = models.BooleanField(default=False, help_text="Si es True, el método es visible para todas las empresas.")


class TransaccionFinanciera(models.Model):
    TIPOS_TRANSACCION = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]

    id_transaccion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='transacciones_financieras')
    fecha_hora_transaccion = models.DateTimeField()
    tipo_transaccion = models.CharField(max_length=20, choices=TIPOS_TRANSACCION)
    monto_transaccion = models.DecimalField(max_digits=18, decimal_places=2)
    id_moneda_transaccion = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='transacciones_moneda')
    id_moneda_base = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='transacciones_base', help_text="Moneda base de la empresa para la transacción.", null=True, blank=True)
    id_moneda_pais_empresa = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='transacciones_pais_empresa', help_text="Moneda país de la empresa para la transacción.", null=True, blank=True)
    monto_moneda_pais = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, help_text="Monto equivalente en moneda país de la empresa.")
    monto_base_empresa = models.DecimalField(max_digits=18, decimal_places=2)
    id_metodo_pago = models.ForeignKey('MetodoPago', on_delete=models.CASCADE, related_name='transacciones')
    referencia_pago = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    tipo_documento_asociado = models.CharField(max_length=20, choices=[
        ('COMPRA', 'Compra'),
        ('VENTA', 'Venta'),
        ('GASTO', 'Gasto'),
        ('NOMINA', 'Nómina'),
        ('AJUSTE', 'Ajuste'),
    ], null=True, blank=True)
    nro_documento_asociado = models.CharField(max_length=100, null=True, blank=True)
    id_caja = models.ForeignKey('Caja', on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones_financieras')
    id_cuenta_bancaria = models.ForeignKey('CuentaBancariaEmpresa', on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones_financieras')
    id_usuario_registro = models.ForeignKey('core.Usuarios', on_delete=models.CASCADE, related_name='transacciones_registradas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finanzas_transaccion_financiera'
        verbose_name = 'Transacción Financiera'
        verbose_name_plural = 'Transacciones Financieras'

    def __str__(self):
        return f"{self.tipo_transaccion} - {self.monto_transaccion}"



# Modelo unificado y flexible para todo tipo de caja (registradora, gerencia, matriz, etc.)

class Caja(models.Model):
    TIPO_CAJA_CHOICES = [
        ('REGISTRADORA', 'Caja Registradora'),
        ('GERENCIA', 'Caja Gerente Sucursal'),
        ('MATRIZ', 'Caja Matriz/Principal'),
        ('OTRO', 'Otro')
    ]

    id_caja = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='cajas', null=True, blank=True)
    sucursal = models.ForeignKey('core.Sucursal', on_delete=models.SET_NULL, null=True, blank=True, related_name='cajas')
    nombre = models.CharField(max_length=100)
    tipo_caja = models.CharField(max_length=20, choices=TIPO_CAJA_CHOICES, default='REGISTRADORA')
    descripcion = models.TextField(blank=True, null=True)
    moneda = models.ForeignKey('Moneda', on_delete=models.CASCADE, related_name='cajas')
    saldo_inicial = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    saldo_actual = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'finanzas_caja'
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_caja_display()}) - {self.moneda.codigo_iso} - {self.saldo_actual}"


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
        ('AJUSTE_POSITIVO', 'Ajuste Positivo'),
        ('AJUSTE_NEGATIVO', 'Ajuste Negativo'),
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