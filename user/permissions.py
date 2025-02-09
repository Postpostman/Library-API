from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only for authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
