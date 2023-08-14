from permissions.permissions import IsAdminOrIfAuthenticatedReadOnly
from rest_framework import viewsets

from borrowing.services.perform_create_borrowing_service import PerformCreateBorrowingService
from borrowing.services.filtering_borrowing_service import FilteringBorrowingService

from book.models import Book
from borrowing.models import Borrowing

from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permissions = [IsAdminOrIfAuthenticatedReadOnly, ]

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff():
            queryset = self.queryset.get(user=self.request.user)

        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("user", "book")

        if FilteringBorrowingService.is_action_valid(self.action):
            service = FilteringBorrowingService(
                queryset=queryset,
                filters=self.request.query_params,
                is_user_staff=self.request.user.is_staff()
            )
            queryset = service.perform()
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        book = Book.objects.get_object_or_404(
            Book,
            id=serializer.book
        )

        service = PerformCreateBorrowingService(
            book=book,
            serializer=BorrowingSerializer,
            action=self.action,
            user=self.request.user
        )
        service.perform()
