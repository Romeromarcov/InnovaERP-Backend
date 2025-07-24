"""
URLs for the Core module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()

# Register ViewSets (to be implemented)
# router.register(r'usuarios', views.UsuarioViewSet)
# router.register(r'empresas', views.EmpresaViewSet)
# router.register(r'sucursales', views.SucursalViewSet)
# router.register(r'departamentos', views.DepartamentoViewSet)
# router.register(r'roles', views.RolViewSet)
# router.register(r'permisos', views.PermisoViewSet)
# router.register(r'monedas', views.MonedaViewSet)

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Custom endpoints
    path('dashboard/kpis/', views.dashboard_kpis_view, name='dashboard_kpis'),
    path('dashboard/stats/', views.dashboard_stats_view, name='dashboard_stats'),
    
    # Placeholder endpoints for testing
    path('usuarios/', views.placeholder_usuarios_view, name='usuarios_list'),
    path('empresas/', views.placeholder_empresas_view, name='empresas_list'),
    path('sucursales/', views.placeholder_sucursales_view, name='sucursales_list'),
    path('departamentos/', views.placeholder_departamentos_view, name='departamentos_list'),
    path('roles/', views.placeholder_roles_view, name='roles_list'),
    path('permisos/', views.placeholder_permisos_view, name='permisos_list'),
    path('monedas/', views.placeholder_monedas_view, name='monedas_list'),
]