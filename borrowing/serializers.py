from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
        ]

    def validate_book(self, value):
        if value.inventory == 0:
            raise ValidationError(
                "We don't have this book right now"
            )
        return value


class BorrowingListSerializer(BorrowingSerializer):
    user = serializers.CharField(
        source="user.email"
    )
    book = serializers.CharField(
        source="book.title"
    )

    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields + ["is_active"]


class BorrowingDetailSerializer(BorrowingListSerializer):
    user = UserSerializer(read_only=True)
    book = BookDetailSerializer(read_only=True)
