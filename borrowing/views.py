from django.db import transaction
from django.utils import timezone
from django_q.tasks import async_task
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer
)
from notification.services import send_notification
from services.create_payment import PaymentService


class BorrowingPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = BorrowingPagination

    def create(self, request, *args, **kwargs):
        borrowing = super(BorrowingViewSet, self).create(request, *args, **kwargs)
        borrowing_data = borrowing.data
        borrowing_headers = borrowing.headers
        response = {
            "borrowing": borrowing_data,
            "url_to_process_payment": self.payment.session_url
        }
        return Response(data=response,
                        status=status.HTTP_201_CREATED,
                        headers=borrowing_headers)

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = self.queryset.filter(user=self.request.user)

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related(
                "user", "book"
            ).prefetch_related(
                "payments"
            )

        if self.action == "list":
            user_id = self.request.query_params.get("user_id")
            is_active = self.request.query_params.get("is_active")

            if user_id:
                queryset = queryset.filter(user_id=user_id)

            if is_active:
                queryset = queryset.filter(is_active=is_active)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "borrowing_return":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            borrowing = serializer.save(user=self.request.user)
            borrowing_permission = PaymentService.check_user_borrowings(
                user=self.request.user,
                book=borrowing.book
            )
            if borrowing_permission:
                raise ValidationError(
                    "You can`t borrow the book, that you already have."
                )
            self.payment = PaymentService(borrowing, self.request).handle()

        book_title = serializer.validated_data['book'].title
        async_task(send_notification,
                   user=self.request.user,
                   message=f"You have initiate borrowing the book {book_title}. "
                           f"You have only 24 hours before payment session expiring.")

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="return",
        permission_classes=[IsAuthenticated, ],
    )
    def borrowing_return(self, request, pk=None):
        borrowing = get_object_or_404(
            Borrowing.objects.filter(user=request.user),
            pk=pk
        )

        if borrowing.is_active:
            borrowing.actual_return_date = timezone.now().date()
            borrowing.save()

            if borrowing.actual_return_date > borrowing.expected_return_date:
                self.payment = PaymentService(borrowing, request).handle()
                return Response(
                    {
                        "Pending": "You have to pay your fine",
                        "payment_url": self.payment.session_url
                    },
                    status=status.HTTP_200_OK
                )

            PaymentService.perform_modifications(
                borrowing=borrowing
            )
            async_task(send_notification,
                       self.request.user,
                       message=f"You have returned a book {borrowing.book.title}.")

            return Response(
                {"Success": "Book returned!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"Fail": "You've returned this book before"},
            status=status.HTTP_404_NOT_FOUND
        )
