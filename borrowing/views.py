from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status

from book.models import Book

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer
)
from services.create_payment import PaymentInitialization


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated, ]

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
            queryset = queryset.select_related("user", "book")

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
        return BorrowingSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            book = serializer.validated_data["book"]
            book.inventory -= 1
            book.save()

            borrowing = serializer.save(user=self.request.user)
            self.payment = PaymentInitialization(borrowing).perform_create_payment()

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
            book = Book.objects.get(id=borrowing.book.id)

            borrowing.is_active = False
            book.inventory += 1
            borrowing.actual_return_date = timezone.now()

            book.save()
            borrowing.save()
            return Response(
                {"Success": "Book returned!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"Fail": "You've returned this book before"},
            status=status.HTTP_404_NOT_FOUND
        )
