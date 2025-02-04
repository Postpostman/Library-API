from rest_framework import viewsets, permissions
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingReadSerializer, BorrowingWriteSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BorrowingReadSerializer
        return BorrowingWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
