from rest_framework import serializers
from borrowing.models import Borrowing
from books.serializers import BookSerializer


class BorrowingReadSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingWriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Borrowing
        fields = "__all__"
