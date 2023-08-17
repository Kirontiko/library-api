from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from book.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    BookImageSerializer,
)
from book.models import Book
from permissions.permissions import IsAdminOrIfAuthenticatedReadOnly


class BookPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


@extend_schema(tags=["Books"])
class BookViewSet(
    ModelViewSet
):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly, ]
    pagination_class = BookPagination

    def get_queryset(self):
        title = self.request.query_params.get("title")
        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookDetailSerializer

        if self.action == "upload_image":
            return BookImageSerializer

        return BookSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific book"""
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                type=str,
                description="Filter by title, lookup=icontains (ex.?title=Harry Potter)",
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
