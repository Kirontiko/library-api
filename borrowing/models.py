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
        ordering = ["-is_active", "expected_return_date"]

    def __str__(self):
        return f"{self.user.email} borrowed {self.book.title} {self.borrow_date}"
