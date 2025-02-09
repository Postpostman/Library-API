from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwner(BasePermission):
    """Only admin or owner can see payments"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.borrowing.user == request.user
