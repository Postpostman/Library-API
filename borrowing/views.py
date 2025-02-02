from rest_framework import viewsets

from borrowing.models import Borrowing
from borrowing.permissions import IsAuthenticated
from borrowing.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):

    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
