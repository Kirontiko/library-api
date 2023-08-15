import os

import stripe
from dotenv import load_dotenv

from payment.models import Payment


load_dotenv()
stripe.api_key = os.environ.get("STRIPE_API_KEY")


class PaymentInitialization:
    CENTS_TO_DOLLARS_MODIFIER = 100
    CURRENCY = "usd"
    QUANTITY = 1

    def __init__(self,
                 borrowing):
        self.borrowing = borrowing

    def create_payment_to_apply_borrowing(self,
                                          session_url,
                                          session_id,
                                          money_to_pay):
        return Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=self.borrowing,
            session_url=session_url,
            session_id=session_id,
            money_to_pay=money_to_pay / 100
        )

    def create_payment_to_process_fine(self,
                                       session_url,
                                       session_id,
                                       money_to_pay):
        return Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=self.borrowing,
            session_url=session_url,
            session_id=session_id,
            money_to_pay=money_to_pay / 100
        )
    def create_checkout_session(self):
        days = self.__calc_days_timedelta(self.borrowing.expected_return_date,
                                          self.borrowing.borrow_date)

        if self.borrowing.actual_return_date:
            days = self.__calc_days_timedelta(self.borrowing.actual_return_date,
                                              self.borrowing.expected_return_date)

        money_to_pay = self.__calc_unit_amount(
                        days,
                        self.borrowing.book.daily_fee
                    )
        session = stripe.checkout.Session.create(
            line_items=[{
                "price_data": {
                    "currency": self.CURRENCY,
                    "product_data": {
                        "name": f"{self.borrowing.book.title} "
                                f"({self.borrowing.book.author})",
                    },
                    "unit_amount": money_to_pay,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://127.0.0.1:8000/api/v1/"
                        "payments/success/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:8000/api/v1/"
                       "payments/cancel",
        )

        return session.url, session.id, money_to_pay

    def perform_create_payment(self):
        session_url, session_id, money_to_pay = self.create_checkout_session()
        if self.borrowing.actual_return_date:
            return self.create_payment_to_process_fine(
                session_url,
                session_id,
                money_to_pay
            )
        return self.create_payment_to_apply_borrowing(
            session_url,
            session_id,
            money_to_pay
        )

    def __calc_unit_amount(self, days, daily_fee):
        return int((daily_fee * days) * self.CENTS_TO_DOLLARS_MODIFIER)

    def __calc_days_timedelta(self, day1, day2):
        return (day1 - day2).days
