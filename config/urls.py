"""
URL configuration for InnovaERP project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.auth_views import (
    CustomTokenObtainPairView,
    login_view,
    logout_view,
    user_profile_view,
    update_profile_view,
    change_password_view,
    refresh_token_view,
    verify_token_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', refresh_token_view, name='token_refresh'),
    path('api/auth/token/verify/', verify_token_view, name='token_verify'),
    path('api/auth/profile/', user_profile_view, name='user_profile'),
    path('api/auth/profile/update/', update_profile_view, name='update_profile'),
    path('api/auth/change-password/', change_password_view, name='change_password'),
    
    # Core module endpoints
    path('api/core/', include('apps.core.urls')),
    
    # Other modules (to be implemented)
    # path('api/inventario/', include('apps.inventario.urls')),
    # path('api/ventas/', include('apps.ventas.urls')),
    # path('api/compras/', include('apps.compras.urls')),
    path('api/finanzas/', include('apps.finanzas.urls')),
    # path('api/crm/', include('apps.crm.urls')),
    # path('api/rrhh/', include('apps.rrhh.urls')),
    path('api/auditoria/', include('apps.auditoria.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)