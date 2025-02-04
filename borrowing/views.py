from rest_framework import viewsets, permissions
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingReadSerializer, BorrowingCreateSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Administrators see all loans, users see only their own."""
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user=user)

    def get_serializer_class(self):
        """Selects the appropriate serializer depending on the action."""
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def perform_create(self, serializer):
        """Assigns `user` before creation."""
        serializer.save(user=self.request.user)
