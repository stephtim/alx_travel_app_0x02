import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing
from decimal import Decimal

# Get the active User model (CustomUser or default User)
User = get_user_model()

class Command(BaseCommand):
    """
    Management command to seed the database with sample Listing data.
    """
    help = 'Seeds the database with sample data for listings.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting database seeding process..."))
        
        # --- 1. Ensure an Owner Exists ---
        try:
            # Try to get an existing superuser or staff user
            owner = User.objects.filter(is_superuser=True).first()
            if not owner:
                owner = User.objects.filter(is_staff=True).first()

            if not owner:
                # If no suitable user exists, create one
                self.stdout.write("Creating a superuser to own the listings...")
                owner = User.objects.create_superuser(
                    username='seeder_admin',
                    email='admin@example.com',
                    password='adminpassword123'
                )
                self.stdout.write(self.style.SUCCESS("Created superuser 'seeder_admin'."))
            else:
                self.stdout.write(f"Using existing user: {owner.username} as listing owner.")
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error setting up user: {e}"))
            return

        # --- 2. Create Sample Listings ---
        
        # Clear existing listings to allow for clean re-seeding
        Listing.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all existing Listing records."))

        listings_data = [
            {
                "title": "Cozy Lakeside Cabin",
                "description": "A quiet retreat nestled by the water, perfect for a peaceful getaway.",
                "price": 120.00,
                "guests": 4,
            },
            {
                "title": "Modern Downtown Loft",
                "description": "Stunning city views and walking distance to all major attractions.",
                "price": 250.50,
                "guests": 2,
            },
            {
                "title": "Spacious Suburban Home",
                "description": "Ideal for large families with a big backyard and close to parks.",
                "price": 185.75,
                "guests": 8,
            },
            {
                "title": "Beachfront Villa",
                "description": "Wake up to the sound of the ocean in this luxury villa.",
                "price": 450.00,
                "guests": 6,
            }
        ]
        
        created_count = 0
        for data in listings_data:
            Listing.objects.create(
                owner=owner,
                title=data['title'],
                description=data['description'],
                price_per_night=Decimal(data['price']),
                max_guests=data['guests'],
                is_available=random.choice([True, True, True, False])
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {created_count} Listing records."
        ))