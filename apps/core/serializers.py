# apps/core/serializers.py
from rest_framework import serializers
class BaseModelSerializer(serializers.ModelSerializer):
    """Serializer base para lógica común y validaciones reutilizables."""
    def validate(self, data):
        # Lógica de validación global aquí si aplica
        return super().validate(data)
from .models import Empresa, Sucursal, Departamento, Usuarios, Roles, Permisos, RolPermisos, UsuarioRoles, RegistroAuditoria
class EmpresaSerializer(BaseModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class SucursalSerializer(BaseModelSerializer):
    id_sucursal = serializers.UUIDField(read_only=True)
    id_empresa = serializers.UUIDField(source='id_empresa.id_empresa')

    class Meta:
        model = Sucursal
        fields = [
            'id_sucursal', 'id_empresa', 'nombre', 'codigo_sucursal', 'direccion', 'telefono',
            'email_contacto', 'ubicacion_gps_json', 'activo', 'fecha_creacion', 'referencia_externa', 'documento_json'
        ]

    def create(self, validated_data):
        # Extraer el UUID de empresa correctamente
        empresa_id = validated_data.pop('id_empresa', None)
        if isinstance(empresa_id, dict):
            empresa_id = empresa_id.get('id_empresa')
        from .models import Empresa
        empresa = Empresa.objects.get(id_empresa=empresa_id)
        sucursal = Sucursal.objects.create(id_empresa=empresa, **validated_data)
        return sucursal

class DepartamentoSerializer(BaseModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class UsuariosSerializer(BaseModelSerializer):
    empresas = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all(), many=True, required=False)
    sucursales = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all(), many=True, required=False)
    departamentos = serializers.PrimaryKeyRelatedField(queryset=Departamento.objects.all(), many=True, required=False)
    roles = serializers.SerializerMethodField()
    es_superusuario_innova = serializers.BooleanField(required=False)

    def get_roles(self, obj):
        from .models import UsuarioRoles
        roles_qs = UsuarioRoles.objects.filter(id_usuario=obj)
        return [
            {
                'id': str(ur.id_rol.id_rol),
                'name': ur.id_rol.nombre_rol
            }
            for ur in roles_qs.select_related('id_rol')
        ]

    def update(self, instance, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        # Solo superusuarios Innova pueden modificar este campo
        if 'es_superusuario_innova' in validated_data:
            if not user or not getattr(user, 'es_superusuario_innova', False):
                validated_data.pop('es_superusuario_innova')
        return super().update(instance, validated_data)

    def create(self, validated_data):
        user = self.context['request'].user if 'request' in self.context else None
        # Solo superusuarios Innova pueden asignar este campo
        if 'es_superusuario_innova' in validated_data:
            if not user or not getattr(user, 'es_superusuario_innova', False):
                validated_data.pop('es_superusuario_innova')
        return super().create(validated_data)

    class Meta:
        model = Usuarios
        fields = '__all__'
        # Si quieres limitar los campos, puedes usar:
        # fields = ['id', 'username', 'email', 'empresas', 'sucursales', ...]

class RolesSerializer(BaseModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class PermisosSerializer(BaseModelSerializer):
    class Meta:
        model = Permisos
        fields = '__all__'

class RolPermisosSerializer(BaseModelSerializer):
    # Para mostrar el nombre del rol y el permiso en lugar de solo los IDs
    id_rol_nombre = serializers.CharField(source='id_rol.nombre_rol', read_only=True)
    id_permiso_nombre = serializers.CharField(source='id_permiso.nombre_permiso', read_only=True)

    class Meta:
        model = RolPermisos
        fields = '__all__'

class UsuarioRolesSerializer(serializers.ModelSerializer):
    # Para mostrar el nombre de usuario y el nombre del rol
    id_usuario_username = serializers.CharField(source='id_usuario.username', read_only=True)
    id_rol_nombre = serializers.CharField(source='id_rol.nombre_rol', read_only=True)

    class Meta:
        model = UsuarioRoles
        fields = '__all__'

class RegistroAuditoriaSerializer(serializers.ModelSerializer):
    # Para mostrar el nombre de usuario que realizó la acción
    id_usuario_username = serializers.CharField(source='id_usuario.username', read_only=True)

    class Meta:
        model = RegistroAuditoria
        fields = '__all__'
        read_only_fields = ('fecha_accion',) # La fecha de acción se genera automáticamente

