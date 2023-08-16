import os

import stripe
from django.urls import reverse
from dotenv import load_dotenv

from payment.models import Payment


load_dotenv()
stripe.api_key = os.environ.get("STRIPE_API_KEY")


class PaymentService:
    CENTS_TO_DOLLARS_MODIFIER = 100
    CURRENCY = "usd"
    QUANTITY = 1

    def __init__(self, borrowing, request):
        self.borrowing = borrowing
        self.request = request


    def handle(self):
        if self.__validate_return_or_create():
            days = self.__calc_days_timedelta(
                self.borrowing.actual_return_date,
                self.borrowing.expected_return_date
            )

        else:
            days = self.__calc_days_timedelta(
                self.borrowing.expected_return_date,
                self.borrowing.borrow_date
            )
        money_to_pay = self.__calc_unit_amount(
            days=days or 1,
            daily_fee=self.borrowing.book.daily_fee
        )

        session_url, session_id = self.__create_checkout_session(
            money_to_pay=money_to_pay
        )

        return self.__create_payment(
            session_url=session_url,
            session_id=session_id,
            money_to_pay=money_to_pay
        )

    def __validate_return_or_create(self):
        return (
                self.borrowing.actual_return_date and
                self.borrowing.actual_return_date > self.borrowing.expected_return_date
        )

    def __calc_days_timedelta(self, day1, day2):
        return (day1 - day2).days

    def __create_payment(
            self,
            session_url,
            session_id,
            money_to_pay
    ):
        payment = Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=self.borrowing,
            session_url=session_url,
            session_id=session_id,
            money_to_pay=money_to_pay / 100
        )
        if self.__validate_return_or_create:
            payment.type = "FINE"
            payment.save()
        return payment

    def __create_checkout_session(self, money_to_pay):
        success_url = self.request.build_absolute_uri(
            reverse("payment:success")
        ) + "?session_id={CHECKOUT_SESSION_ID}"
        cancel_url = self.request.build_absolute_uri(reverse("payment:cancel"))

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": self.CURRENCY,
                        "product_data": {
                            "name": f"{self.borrowing.book.title} "
                                    f"({self.borrowing.book.author})",
                        },
                        "unit_amount": money_to_pay,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,

            cancel_url=cancel_url
        )

        return session.url, session.id

    def __calc_unit_amount(self, days, daily_fee):
        return int((daily_fee * days) * self.CENTS_TO_DOLLARS_MODIFIER)

    @classmethod
    def perform_modifications(cls, borrowing):
        book = borrowing.book

        if borrowing.actual_return_date:
            borrowing.is_active = False
            book.inventory += 1
        else:
            book.inventory -= 1
        borrowing.save()
        book.save()

    @classmethod
    def check_user_borrowings(cls, user, book):
        return user.borrowings.filter(
            book=book,
            is_active=True
        ).count() > 1
