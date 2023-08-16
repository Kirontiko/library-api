import datetime
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django_q.tasks import async_task
from notification.services import send_notification


def send_daily_notifications():
    User = get_user_model()
    users = User.objects.all()
    print(users)

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

        if delayed_books:
            message = f"You forgot to return book(s): {delayed_books}"
            async_task(send_notification, user, message)


def send_notification_remind_return():
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        books = []
        borrowing_books = user.borrowings.filter(
            is_active=True
        )
        if user.chat_id:
            for borrowing in borrowing_books:
                date_difference = (
                        borrowing.expected_return_date - datetime.date.today()
                )
                if date_difference.days == 1:
                    print(date_difference.days)
                    books.append(borrowing.book.title)

        if books:
            message = f"Remind tomorrow you need to return: {books}"
            async_task(send_notification, user, message)
