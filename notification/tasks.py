import datetime
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from borrowing.models import Borrowing


from django.contrib.auth import get_user_model
from django_q.tasks import async_task
from notification.services import send_notification


def send_daily_notifications():
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        if user.chat_id:
            print(user.chat_id)
            message = "It's an every 10 minutes message (:"

            async_task(send_notification, user, message)


def send_notification_delayed_return():
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        delayed_books = []
        borrowing_books = user.borrowings.filter(
            is_active=True
        )
        if user.chat_id:
            for borrowing in borrowing_books:
                if borrowing.expected_return_date < datetime.date.today():

                    delayed_books.append(borrowing.book.title)

        message = f"You forgot to return book(s): {delayed_books}"
        if delayed_books:
            async_task(send_notification, user, message)


def send_daily_staff_notifications():
    delayed_users = set()
    User = get_user_model()
    staff = User.objects.filter(
        is_staff=True
    )
    borrowing = Borrowing.objects.all()

    for librarian in staff:
        for borrow in borrowing:
            if borrow.expected_return_date < datetime.date.today():
                delayed_users.add(borrow.user.email)

        if delayed_users:
            message = f"This users delayed their books: {delayed_users}"
            async_task(send_notification, librarian, message)
        else:
            message = "We dont have any borrowers :)"
            async_task(send_notification, librarian, message)
