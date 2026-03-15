from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    """Apenas superusuários podem acessar."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
