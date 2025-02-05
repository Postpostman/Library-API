from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingCreateSerializer, BorrowingReadSerializer


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

    @action(detail=True, methods=["POST"], url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.is_returned:
            return Response({"error": "This book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

        borrowing.actual_return_day = now().date()
        borrowing.is_returned = True
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        return Response({"message": "Book successfully returned!"}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
