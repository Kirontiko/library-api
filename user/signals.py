from django.dispatch import receiver
from secrets import token_urlsafe
from .models import User

from django.db.models.signals import post_migrate, pre_save
from django_q.tasks import schedule
from django_q.models import Schedule


@receiver(pre_save, sender=User)
def generate_telegram_token_before_save(sender, instance, **kwargs):
    if not instance.token:
        instance.token = token_urlsafe(8)


@receiver(post_migrate)
def create_schedules(sender, **kwargs):
    if sender.name == 'user':
        if not Schedule.objects.filter(name='check borrowers').exists():
            schedule(
                func="notification.tasks.send_daily_notifications",
                name="check borrowers",
                repeats=-1,
                schedule_type=Schedule.MINUTES,
                minutes=10,
            )

        if not Schedule.objects.filter(name='delayed borrowers').exists():
            schedule(
                func="notification.tasks.send_notification_delayed_return",
                name="delayed borrowers",
                repeats=-1,
                schedule_type=Schedule.DAILY,
            )

        if not Schedule.objects.filter(name='list of borrowers').exists():
            schedule(
                func="notification.tasks.send_daily_staff_notifications",
                name="list of borrowers",
                repeats=-1,
                schedule_type=Schedule.DAILY,
            )

        if not Schedule.objects.filter(name='remind borrowers').exists():
            schedule(
                func="notification.tasks.send_notification_delayed_return",
                name="remind borrowers",
                repeats=-1,
                schedule_type=Schedule.DAILY,
            )
