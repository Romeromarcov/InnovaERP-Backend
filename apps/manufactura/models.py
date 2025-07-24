from django.db import models
from apps.inventario.models import Producto
import uuid

class ListaMateriales(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, null=True, blank=True)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    producto_final = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='listas_materiales')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class RutaProduccion(models.Model):
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, null=True, blank=True)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class OrdenProduccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, null=True, blank=True)
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    tipo_operacion = models.CharField(max_length=50, null=True, blank=True)
    fecha_cierre_estimada = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('en_proceso', 'En Proceso'), ('finalizada', 'Finalizada'), ('cancelada', 'Cancelada'), ('parcial', 'Parcial')], default='pendiente')
    lista_materiales = models.ForeignKey(ListaMateriales, on_delete=models.SET_NULL, null=True, blank=True)
    ruta_produccion = models.ForeignKey(RutaProduccion, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"OP-{self.id} {self.producto} ({self.estado})"

class ConsumoMaterial(models.Model):
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name='consumos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x {self.cantidad} (OP {self.orden_produccion.id})"

class ProduccionTerminada(models.Model):
    referencia_externa = models.CharField(max_length=100, null=True, blank=True)
    documento_json = models.JSONField(null=True, blank=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, related_name='produccion_terminada')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} terminado OP {self.orden_produccion.id}"


class ListaMaterialesDetalle(models.Model):
    id_detalle_lista = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_lista_materiales = models.ForeignKey('ListaMateriales', on_delete=models.CASCADE, related_name='detalles')
    id_producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='detalles_lista_materiales')
    cantidad_requerida = models.DecimalField(max_digits=18, decimal_places=4)
    id_unidad_medida = models.ForeignKey('inventario.UnidadMedida', on_delete=models.CASCADE, related_name='detalles_lista_materiales')
    es_opcional = models.BooleanField(default=False)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'manufactura_lista_materiales_detalle'
        verbose_name = 'Detalle de Lista de Materiales'
        verbose_name_plural = 'Detalles de Lista de Materiales'

    def __str__(self):
        return f"{self.id_lista_materiales.nombre} - {self.id_producto.nombre_producto}"


class CentroTrabajo(models.Model):
    id_centro_trabajo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='centros_trabajo')
    codigo_centro = models.CharField(max_length=50, unique=True)
    nombre_centro = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    tipo_centro = models.CharField(max_length=20, choices=[
        ('MAQUINA', 'Máquina'),
        ('MANUAL', 'Manual'),
        ('ENSAMBLE', 'Ensamble'),
        ('CONTROL_CALIDAD', 'Control de Calidad'),
        ('EMPAQUE', 'Empaque')
    ])
    capacidad_horas_dia = models.DecimalField(max_digits=8, decimal_places=2, default=8.00)
    costo_hora = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'manufactura_centro_trabajo'
        verbose_name = 'Centro de Trabajo'
        verbose_name_plural = 'Centros de Trabajo'

    def __str__(self):
        return f"{self.codigo_centro} - {self.nombre_centro}"


class OperacionProduccion(models.Model):
    id_operacion = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_empresa = models.ForeignKey('core.Empresa', on_delete=models.CASCADE, related_name='operaciones_produccion')
    codigo_operacion = models.CharField(max_length=50, unique=True)
    nombre_operacion = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    tiempo_estandar_minutos = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'manufactura_operacion_produccion'
        verbose_name = 'Operación de Producción'
        verbose_name_plural = 'Operaciones de Producción'

    def __str__(self):
        return f"{self.codigo_operacion} - {self.nombre_operacion}"


class RutaProduccionDetalle(models.Model):
    id_detalle_ruta = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_ruta_produccion = models.ForeignKey('RutaProduccion', on_delete=models.CASCADE, related_name='detalles')
    id_operacion = models.ForeignKey('OperacionProduccion', on_delete=models.CASCADE, related_name='detalles_ruta')
    id_centro_trabajo = models.ForeignKey('CentroTrabajo', on_delete=models.CASCADE, related_name='detalles_ruta')
    numero_secuencia = models.IntegerField()
    tiempo_preparacion_minutos = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    tiempo_operacion_minutos = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'manufactura_ruta_produccion_detalle'
        verbose_name = 'Detalle de Ruta de Producción'
        verbose_name_plural = 'Detalles de Ruta de Producción'
        ordering = ['numero_secuencia']

    def __str__(self):
        return f"{self.id_ruta_produccion.nombre} - Paso {self.numero_secuencia}: {self.id_operacion.nombre_operacion}"


class RegistroOperacion(models.Model):
    id_registro = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_orden_produccion = models.ForeignKey('OrdenProduccion', on_delete=models.CASCADE, related_name='registros_operacion')
    id_detalle_ruta = models.ForeignKey('RutaProduccionDetalle', on_delete=models.CASCADE, related_name='registros')
    id_empleado = models.ForeignKey('rrhh.Empleado', on_delete=models.CASCADE, related_name='registros_operacion')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    cantidad_procesada = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    cantidad_defectuosa = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    estado = models.CharField(max_length=20, choices=[
        ('INICIADO', 'Iniciado'),
        ('EN_PROGRESO', 'En Progreso'),
        ('PAUSADO', 'Pausado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ], default='INICIADO')
    observaciones = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'manufactura_registro_operacion'
        verbose_name = 'Registro de Operación'
        verbose_name_plural = 'Registros de Operaciones'

    def __str__(self):
        return f"OP-{self.id_orden_produccion.id} - {self.id_detalle_ruta.id_operacion.nombre_operacion} - {self.estado}"
