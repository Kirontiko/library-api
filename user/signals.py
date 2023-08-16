from django.db.models.signals import pre_save
from django.dispatch import receiver
from secrets import token_urlsafe
from .models import User


@receiver(pre_save, sender=User)
def generate_telegram_token_before_save(sender, instance, **kwargs):
    if not instance.token:
        instance.token = token_urlsafe(8)
