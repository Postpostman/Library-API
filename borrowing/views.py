from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingReadSerializer, BorrowingCreateSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["is_returned"]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                return Borrowing.objects.filter(user_id=user_id)
            return Borrowing.objects.all()

        return Borrowing.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
