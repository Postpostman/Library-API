# users/permissions.py
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Permission for checking is user owner or not
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
