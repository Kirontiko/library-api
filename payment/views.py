from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment.models import Payment
from payment.serializers import PaymentListSerializer, PaymentSerializer
from services.create_payment import PaymentService


class PaymentPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Payment.objects.select_related(
        "borrowing__book",
        "borrowing__user"
    )
    permission_classes = [IsAuthenticated, ]
    pagination_class = PaymentPagination

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer

        return PaymentSerializer

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAuthenticated, ],
        url_path="success"
    )
    def success(self, request):
        session_id = self.request.query_params.get("session_id")
        payment = Payment.objects.get(session_id=session_id)

        borrowing = payment.borrowing
        PaymentService.perform_modifications(borrowing)

        payment.status = "PAID"
        payment.save()

        return Response(
            {
                "success": "The payment was successful"
            },
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAuthenticated, ],
        url_path="cancel"
    )
    def cancel(self, request):
        return Response(
            {
                "failed": "Payment can be paid a bit later "
                          "(but the session is available for only 24h)"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
