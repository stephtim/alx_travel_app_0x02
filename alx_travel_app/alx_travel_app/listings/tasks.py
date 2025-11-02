# listings/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(customer_email, booking_id):
    subject = f"Booking Confirmation #{booking_id}"
    message = f"Hello, your booking #{booking_id} has been confirmed. Thank you!"
    from_email = 'noreply@travelapp.com'
    
    send_mail(subject, message, from_email, [customer_email])
    return f"Email sent to {customer_email}"
