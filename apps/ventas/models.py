from django.db import models
import uuid

class Pedido(models.Model):
    id_pedido = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE)
    id_cliente = models.ForeignKey('crm.Cliente', on_delete=models.CASCADE)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    tipo_operacion = models.CharField(max_length=50, null=True, blank=True)
    fecha_cierre_estimada = models.DateField(null=True, blank=True)
    numero_pedido = models.CharField(max_length=50, unique=True)
    fecha_pedido = models.DateField()
    estado = models.CharField(max_length=30, choices=[
        ('BORRADOR', 'Borrador'),
        ('ENVIADO', 'Enviado'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
        ('CERRADO', 'Cerrado'),
        ('ANULADO', 'Anulado')
    ], default='BORRADOR')
    observaciones = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_pedido

class DetallePedido(models.Model):
    id_detalle_pedido = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    observaciones = models.TextField(null=True, blank=True)

class NotaVenta(models.Model):
    id_nota_venta = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE)
    id_cliente = models.ForeignKey('crm.Cliente', on_delete=models.CASCADE)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    numero_nota = models.CharField(max_length=50, unique=True)
    fecha_nota = models.DateField()
    estado = models.CharField(max_length=30, choices=[
        ('BORRADOR', 'Borrador'),
        ('ENTREGADA', 'Entregada'),
        ('FACTURADA', 'Facturada'),
        ('ANULADA', 'Anulada')
    ], default='BORRADOR')
    observaciones = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_nota

class DetalleNotaVenta(models.Model):
    id_detalle_nota_venta = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_nota_venta = models.ForeignKey(NotaVenta, related_name='detalles', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    observaciones = models.TextField(null=True, blank=True)

class Factura(models.Model):
    id_factura = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE)
    id_cliente = models.ForeignKey('crm.Cliente', on_delete=models.CASCADE)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField()
    monto_total = models.DecimalField(max_digits=18, decimal_places=4)
    observaciones = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_factura


class Cotizacion(models.Model):
    id_cotizacion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='cotizaciones')
    id_cliente = models.ForeignKey('crm.Cliente', on_delete=models.CASCADE, related_name='cotizaciones')
    numero_cotizacion = models.CharField(max_length=50, unique=True)
    fecha_cotizacion = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=30, choices=[
        ('BORRADOR', 'Borrador'),
        ('ENVIADA', 'Enviada'),
        ('ACEPTADA', 'Aceptada'),
        ('RECHAZADA', 'Rechazada'),
        ('VENCIDA', 'Vencida'),
        ('ANULADA', 'Anulada')
    ], default='BORRADOR')
    monto_total = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    id_moneda = models.ForeignKey('finanzas.Moneda', on_delete=models.CASCADE, related_name='cotizaciones')
    observaciones = models.TextField(null=True, blank=True)
    condiciones_comerciales = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ventas_cotizacion'
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'

    def __str__(self):
        return self.numero_cotizacion


class DetalleCotizacion(models.Model):
    id_detalle_cotizacion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_cotizacion = models.ForeignKey('Cotizacion', related_name='detalles', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='detalles_cotizacion')
    id_variante = models.ForeignKey('inventario.VarianteProducto', on_delete=models.CASCADE, null=True, blank=True, related_name='detalles_cotizacion')
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=4)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    descuento_monto = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ventas_detalle_cotizacion'
        verbose_name = 'Detalle de Cotización'
        verbose_name_plural = 'Detalles de Cotización'

    def __str__(self):
        return f"{self.id_cotizacion.numero_cotizacion} - {self.id_producto.nombre_producto}"


class DetalleFactura(models.Model):
    id_detalle_factura = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_factura = models.ForeignKey('Factura', related_name='detalles', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='detalles_factura')
    id_variante = models.ForeignKey('inventario.VarianteProducto', on_delete=models.CASCADE, null=True, blank=True, related_name='detalles_factura')
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=4)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    descuento_monto = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    monto_impuesto = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    total_linea = models.DecimalField(max_digits=18, decimal_places=4)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ventas_detalle_factura'
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Factura'

    def __str__(self):
        return f"{self.id_factura.numero_factura} - {self.id_producto.nombre_producto}"


class NotaCreditoVenta(models.Model):
    id_nota_credito = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='notas_credito_venta')
    id_cliente = models.ForeignKey('crm.Cliente', on_delete=models.CASCADE, related_name='notas_credito')
    id_factura_origen = models.ForeignKey('Factura', on_delete=models.CASCADE, null=True, blank=True, related_name='notas_credito')
    numero_nota_credito = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField()
    motivo = models.CharField(max_length=20, choices=[
        ('DEVOLUCION', 'Devolución'),
        ('DESCUENTO', 'Descuento'),
        ('ERROR_FACTURACION', 'Error de Facturación'),
        ('ANULACION', 'Anulación'),
        ('OTRO', 'Otro')
    ])
    monto_total = models.DecimalField(max_digits=18, decimal_places=4)
    id_moneda = models.ForeignKey('finanzas.Moneda', on_delete=models.CASCADE, related_name='notas_credito_venta')
    estado = models.CharField(max_length=20, choices=[
        ('BORRADOR', 'Borrador'),
        ('EMITIDA', 'Emitida'),
        ('APLICADA', 'Aplicada'),
        ('ANULADA', 'Anulada')
    ], default='BORRADOR')
    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ventas_nota_credito_venta'
        verbose_name = 'Nota de Crédito de Venta'
        verbose_name_plural = 'Notas de Crédito de Venta'

    def __str__(self):
        return self.numero_nota_credito


class DetalleNotaCreditoVenta(models.Model):
    id_detalle_nota_credito = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_nota_credito = models.ForeignKey('NotaCreditoVenta', related_name='detalles', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='detalles_nota_credito')
    id_variante = models.ForeignKey('inventario.VarianteProducto', on_delete=models.CASCADE, null=True, blank=True, related_name='detalles_nota_credito')
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    monto_impuesto = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    total_linea = models.DecimalField(max_digits=18, decimal_places=4)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ventas_detalle_nota_credito_venta'
        verbose_name = 'Detalle de Nota de Crédito'
        verbose_name_plural = 'Detalles de Nota de Crédito'

    def __str__(self):
        return f"{self.id_nota_credito.numero_nota_credito} - {self.id_producto.nombre_producto}"


class DevolucionVenta(models.Model):
    id_devolucion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='devoluciones_venta')
    id_cliente = models.ForeignKey('crm.Cliente', on_delete=models.CASCADE, related_name='devoluciones')
    id_factura_origen = models.ForeignKey('Factura', on_delete=models.CASCADE, null=True, blank=True, related_name='devoluciones')
    numero_devolucion = models.CharField(max_length=50, unique=True)
    fecha_devolucion = models.DateField()
    motivo_devolucion = models.CharField(max_length=20, choices=[
        ('DEFECTO', 'Defecto'),
        ('GARANTIA', 'Garantía'),
        ('ERROR_ENTREGA', 'Error de Entrega'),
        ('CAMBIO_CLIENTE', 'Cambio de Cliente'),
        ('VENCIMIENTO', 'Vencimiento'),
        ('OTRO', 'Otro')
    ])
    estado = models.CharField(max_length=20, choices=[
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('PROCESADA', 'Procesada'),
        ('RECHAZADA', 'Rechazada'),
        ('ANULADA', 'Anulada')
    ], default='PENDIENTE')
    monto_total = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    id_moneda = models.ForeignKey('finanzas.Moneda', on_delete=models.CASCADE, related_name='devoluciones_venta')
    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ventas_devolucion_venta'
        verbose_name = 'Devolución de Venta'
        verbose_name_plural = 'Devoluciones de Venta'

    def __str__(self):
        return self.numero_devolucion


class DetalleDevolucionVenta(models.Model):
    id_detalle_devolucion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_devolucion = models.ForeignKey('DevolucionVenta', related_name='detalles', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='detalles_devolucion')
    id_variante = models.ForeignKey('inventario.VarianteProducto', on_delete=models.CASCADE, null=True, blank=True, related_name='detalles_devolucion')
    cantidad_devuelta = models.DecimalField(max_digits=18, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    estado_producto = models.CharField(max_length=20, choices=[
        ('BUENO', 'Bueno'),
        ('DEFECTUOSO', 'Defectuoso'),
        ('VENCIDO', 'Vencido'),
        ('DAÑADO', 'Dañado')
    ])
    accion_inventario = models.CharField(max_length=20, choices=[
        ('REINTEGRAR', 'Reintegrar a Stock'),
        ('CUARENTENA', 'Enviar a Cuarentena'),
        ('DESCARTAR', 'Descartar'),
        ('REPARAR', 'Enviar a Reparación')
    ])
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ventas_detalle_devolucion_venta'
        verbose_name = 'Detalle de Devolución'
        verbose_name_plural = 'Detalles de Devolución'

    def __str__(self):
        return f"{self.id_devolucion.numero_devolucion} - {self.id_producto.nombre_producto}"
