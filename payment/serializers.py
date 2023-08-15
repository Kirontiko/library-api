from rest_framework import serializers

from borrowing.serializers import (
    BorrowingDetailSerializer,
    BorrowingListSerializer)
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "status", "type", "borrowing",
                  "session_url", "session_id", "money_to_pay")


class PaymentDetailSerializer(PaymentSerializer):
    borrowing = BorrowingDetailSerializer(read_only=True, many=False)


class PaymentListSerializer(PaymentSerializer):
    borrowing = BorrowingListSerializer(read_only=True, many=False)
