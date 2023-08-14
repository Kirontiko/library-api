from rest_framework import serializers
from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id",
                  "title",
                  "author",
                  "cover",
                  "daily_fee",
                  "inventory", )


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id",
                  "title",
                  "author",
                  "daily_fee",
                  "image", )


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id",
                  "title",
                  "author",
                  "cover",
                  "inventory",
                  "daily_fee",
                  "image", )


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id",
                  "image", )
