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
    class Meta:
        model = Sucursal
        fields = '__all__'

class DepartamentoSerializer(BaseModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class UsuariosSerializer(BaseModelSerializer):
    empresas = EmpresaSerializer(many=True, read_only=True)
    sucursales = SucursalSerializer(many=True, read_only=True)

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

