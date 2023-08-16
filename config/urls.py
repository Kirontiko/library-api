from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("book.urls", namespace="book")),
    path("api/v1/users/", include("user.urls", namespace="user")),
    path("api/v1/borrowings/", include("borrowing.urls", namespace="borrowing")),
    path("api/v1/payments/", include("payment.urls", namespace="payment"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django_q.tasks import schedule
from django_q.models import Schedule

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
