from rest_framework import serializers
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Borrowing
        fields = "__all__"
