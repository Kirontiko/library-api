from django.db import models


class Book(models.Model):
    COVER_CHOICES = [
        ("HARD", "Hard"),
        ("SOFT", "Soft"),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField()

    def __str__(self):
        return self.title
