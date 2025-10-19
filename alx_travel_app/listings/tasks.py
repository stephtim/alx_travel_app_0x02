from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_confirmation_email(user_email, booking_reference, amount):
    subject = "Payment Confirmation"
    message = f"Your payment for booking {booking_reference} of amount {amount} has been successfully completed."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
