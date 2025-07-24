"""
Views for the Core module
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_kpis_view(request):
    """
    Dashboard KPIs endpoint
    """
    # Mock data for now - replace with real calculations
    kpis = {
        'totalRevenue': 125000,
        'revenueChange': '+12.5%',
        'revenueChangeType': 'positive',
        'openOrders': 45,
        'ordersChange': '+8%',
        'ordersChangeType': 'positive',
        'inventoryValue': 89000,
        'inventoryChange': '-2.1%',
        'inventoryChangeType': 'negative',
        'pendingApprovals': 12,
        'approvalsChange': '+3',
        'approvalsChangeType': 'neutral'
    }
    
    return Response(kpis, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats_view(request):
    """
    Dashboard statistics endpoint
    """
    # Mock data for now
    stats = {
        'sales_this_month': 45000,
        'sales_last_month': 38000,
        'new_customers': 15,
        'active_users': User.objects.filter(is_active=True).count(),
        'total_products': 250,
        'low_stock_items': 8
    }
    
    return Response(stats, status=status.HTTP_200_OK)

# Placeholder views for testing - replace with proper ViewSets later

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def placeholder_usuarios_view(request):
    """Placeholder for usuarios endpoint"""
    if request.method == 'GET':
        # Mock users data
        users = [
            {
                'id': 1,
                'username': 'admin',
                'email': 'admin@innovaerp.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_active': True,
                'id_empresa': 1,
                'id_sucursal_predeterminada': 1,
                'es_superusuario_innova': True
            },
            {
                'id': 2,
                'username': 'usuario1',
                'email': 'usuario1@innovaerp.com',
                'first_name': 'Usuario',
                'last_name': 'Prueba',
                'is_active': True,
                'id_empresa': 1,
                'id_sucursal_predeterminada': 1,
                'es_superusuario_innova': False
            }
        ]
        return Response(users, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Mock user creation
        return Response({
            'id': 3,
            'message': 'Usuario creado exitosamente (mock)'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def placeholder_empresas_view(request):
    """Placeholder for empresas endpoint"""
    if request.method == 'GET':
        empresas = [
            {
                'id': 1,
                'nombre_legal': 'InnovaERP S.A.',
                'identificador_fiscal': '12345678901',
                'direccion_fiscal': 'Av. Principal 123, Ciudad',
                'telefono': '+1234567890',
                'id_moneda_base': 1
            }
        ]
        return Response(empresas, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        return Response({
            'id': 2,
            'message': 'Empresa creada exitosamente (mock)'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def placeholder_sucursales_view(request):
    """Placeholder for sucursales endpoint"""
    if request.method == 'GET':
        sucursales = [
            {
                'id': 1,
                'nombre': 'Sucursal Principal',
                'direccion': 'Av. Principal 123, Ciudad',
                'telefono': '+1234567890',
                'email': 'principal@innovaerp.com',
                'id_empresa': 1,
                'es_activa': True
            }
        ]
        return Response(sucursales, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        return Response({
            'id': 2,
            'message': 'Sucursal creada exitosamente (mock)'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def placeholder_departamentos_view(request):
    """Placeholder for departamentos endpoint"""
    if request.method == 'GET':
        departamentos = [
            {
                'id': 1,
                'nombre': 'Administración',
                'descripcion': 'Departamento de administración general',
                'id_sucursal': 1,
                'es_activo': True
            },
            {
                'id': 2,
                'nombre': 'Ventas',
                'descripcion': 'Departamento de ventas y marketing',
                'id_sucursal': 1,
                'es_activo': True
            }
        ]
        return Response(departamentos, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        return Response({
            'id': 3,
            'message': 'Departamento creado exitosamente (mock)'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def placeholder_roles_view(request):
    """Placeholder for roles endpoint"""
    if request.method == 'GET':
        roles = [
            {
                'id': 1,
                'nombre': 'Administrador',
                'descripcion': 'Acceso completo al sistema',
                'es_activo': True
            },
            {
                'id': 2,
                'nombre': 'Usuario',
                'descripcion': 'Acceso básico al sistema',
                'es_activo': True
            }
        ]
        return Response(roles, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        return Response({
            'id': 3,
            'message': 'Rol creado exitosamente (mock)'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def placeholder_permisos_view(request):
    """Placeholder for permisos endpoint"""
    if request.method == 'GET':
        permisos = [
            {
                'id': 1,
                'nombre': 'usuarios.crear',
                'descripcion': 'Crear usuarios',
                'modulo': 'core',
                'accion': 'crear',
                'es_activo': True
            },
            {
                'id': 2,
                'nombre': 'usuarios.leer',
                'descripcion': 'Ver usuarios',
                'modulo': 'core',
                'accion': 'leer',
                'es_activo': True
            }
        ]
        return Response(permisos, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        return Response({
            'id': 3,
            'message': 'Permiso creado exitosamente (mock)'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def placeholder_monedas_view(request):
    """Placeholder for monedas endpoint"""
    if request.method == 'GET':
        monedas = [
            {
                'id': 1,
                'nombre': 'Dólar Estadounidense',
                'codigo_iso': 'USD',
                'simbolo': '$',
                'es_activa': True
            },
            {
                'id': 2,
                'nombre': 'Euro',
                'codigo_iso': 'EUR',
                'simbolo': '€',
                'es_activa': True
            },
            {
                'id': 3,
                'nombre': 'Peso Mexicano',
                'codigo_iso': 'MXN',
                'simbolo': '$',
                'es_activa': True
            }
        ]
        return Response(monedas, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        return Response({
            'id': 4,
            'message': 'Moneda creada exitosamente (mock)'
        }, status=status.HTTP_201_CREATED)