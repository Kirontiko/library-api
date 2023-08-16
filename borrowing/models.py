from django.db import models

from user.models import User
from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-expected_return_date"]

    def __str__(self):
        return f"{self.user.email} borrowed {self.book.title} {self.borrow_date}"

    @staticmethod
    def validate_expected_return_date(expected_return_date, minimum_return_date, error_to_raise):
        if not (expected_return_date >= minimum_return_date):
            raise error_to_raise("Return data can't be in the past")
