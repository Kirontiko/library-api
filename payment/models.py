from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
    ]
    TYPE_CHOICES = [
        ("PAYMENT", "Payment"),
        ("FINE", "Fine"),
    ]
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=7)
    type = models.CharField(choices=TYPE_CHOICES,
                            max_length=7)
    borrowing = models.ForeignKey(Borrowing,
                                  related_name="payments",
                                  on_delete=models.CASCADE)
    session_url = models.URLField(null=True)
    session_id = models.CharField(max_length=255,
                                  null=True,
                                  blank=True)
    money_to_pay = models.DecimalField(decimal_places=2,
                                       max_digits=8)
