from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay"
        )


class PaymentListSerializer(PaymentSerializer):
    borrowed_book = serializers.CharField(
        source="borrowing.book.title",
        read_only=True
    )

    class Meta(PaymentSerializer.Meta):
        fields = PaymentSerializer.Meta.fields + (
            "borrowed_book",
        )


class PaymentDetailSerializer(PaymentListSerializer):
    borrow_date = serializers.DateField(
        source="borrowing.borrow_date",
        read_only=True
    )
    borrowing_expected_return_date = serializers.DateField(
        source="borrowing.expected_return_date",
        read_only=True
    )
    borrowing_actual_return_date = serializers.DateField(
        source="borrowing.actual_return_date",
        read_only=True
    )
    borrowing_is_active = serializers.BooleanField(
        source="borrowing.is_active",
        read_only=True
    )

    class Meta(PaymentListSerializer.Meta):
        fields = PaymentListSerializer.Meta.fields + (
            "borrow_date",
            "borrowing_expected_return_date",
            "borrowing_actual_return_date",
            "borrowing_is_active"
        )
