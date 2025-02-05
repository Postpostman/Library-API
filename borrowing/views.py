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
        queryset = Borrowing.objects.all()

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            if is_active.lower() == "true":
                queryset = queryset.filter(is_returned=False)
            elif is_active.lower() == "false":
                queryset = queryset.filter(is_returned=True)

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
