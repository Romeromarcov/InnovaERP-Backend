from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """Permite solo lectura a usuarios normales y escritura solo a admins."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
