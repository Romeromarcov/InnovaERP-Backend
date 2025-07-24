from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination

class BaseModelViewSet(viewsets.ModelViewSet):
    """ViewSet base para CRUD genérico con paginación, búsqueda y permisos estándar."""
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = '__all__'
    ordering_fields = '__all__'
