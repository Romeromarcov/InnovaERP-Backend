# --- Desactivar CSRF en DRF para desarrollo ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'config.settings_dev.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

from rest_framework.authentication import SessionAuthentication
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # No-op para desarrollo

# --- Sobreescribir MIDDLEWARE para desarrollo (sin CSRF) ---
from .settings_base import *
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # Desactivado para desarrollo
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# Permitir frontend local como origen confiable para CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
]

# Si usas django-cors-headers, permite también el origen para CORS
try:
    CORS_ALLOWED_ORIGINS.append("http://localhost:5173")
    CORS_ALLOWED_ORIGINS.append("http://localhost:5174")
except Exception:
    CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://localhost:5174"]
