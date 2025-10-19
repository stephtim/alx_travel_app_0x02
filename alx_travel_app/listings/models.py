from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Listing(models.Model):
    """Represents a property listing."""
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='listings'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    max_guests = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    """Represents a reservation for a listing."""
    
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a guest cannot book the same listing for overlapping dates
        unique_together = ('listing', 'check_in_date', 'check_out_date')

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.guest.username}"

class Review(models.Model):
    """Represents a review for a listing."""
    
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures one user can only review a listing once
        unique_together = ('listing', 'reviewer') 
        
    def __str__(self):
        return f"Review for {self.listing.title} ({self.rating}/5)"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    booking_reference = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique reference for the booking this payment belongs to"
    )
    transaction_id = models.CharField(
        max_length=150,
        unique=True,
        help_text="Transaction ID returned by the payment gateway (e.g., Chapa)"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount paid in the selected currency"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        help_text="Current status of the payment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the payment record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the payment record was last updated"
    )

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"