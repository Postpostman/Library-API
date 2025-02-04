from rest_framework import serializers
from borrowing.models import Borrowing
from books.models import Book


class BorrowingReadSerializer(serializers.ModelSerializer):
    """Read-serializer for viewing the list and details of borrowings."""
    user = serializers.ReadOnlyField(source="user.id")
    book = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = "__all__"

    def get_book(self, obj):
        """Returns detailed information about the book"""
        return {
            "id": obj.book.id,
            "title": obj.book.title,
            "author": obj.book.author,
            "daily_fee": obj.book.daily_fee,
        }


class BorrowingCreateSerializer(serializers.ModelSerializer):
    """Write-serializer for creating a new loan."""

    class Meta:
        model = Borrowing
        fields = ["borrow_date", "expected_return_date", "book"]

    def validate_book(self, book):
        """Checks if the book is available."""
        if book.inventory < 1:
            raise serializers.ValidationError("This book is out of stock.")
        return book

    def create(self, validated_data):
        """Creates a loan, reduces `inventory` and adds a user."""
        book = validated_data["book"]
        book.inventory -= 1
        book.save()

        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing
