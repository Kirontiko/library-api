from django.utils import timezone
from book.serializers import BookDetailSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowing.models import Borrowing
from user.serializers import UserSerializer
import datetime


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        ]

    def validate_book(self, value):
        if value.inventory == 0:
            raise ValidationError(
                "We don't have this book right now"
            )
        return value

    def validate_expected_return_date(self, value):
        if value <= timezone.now().date():
            raise ValidationError(
                "You cannot set expected return date as the current date "
                "or earlier date"
            )
        return value


class BorrowingListSerializer(BorrowingSerializer):
    user = serializers.CharField(
        source="user.email", read_only=True
    )
    book = serializers.CharField(
        source="book.title", read_only=True
    )

    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields + ["is_active", "user"]


class BorrowingDetailSerializer(BorrowingListSerializer):
    user = UserSerializer(read_only=True)
    book = BookDetailSerializer(read_only=True)


class BorrowingReturnSerializer(BorrowingListSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        ]
        read_only_fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        ]
