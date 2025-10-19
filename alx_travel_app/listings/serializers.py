from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.
    Read-only fields display related data clearly (e.g., owner's username).
    """
    
    # Use ReadOnlyField to display the owner's username instead of the primary key (ID).
    owner = serializers.ReadOnlyField(source='owner.username') 
    
    # Optional: If you wanted to include the number of reviews
    # reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'owner', 'title', 'description', 
            'price_per_night', 'max_guests', 'is_available', 
            'created_at'
        ]
        # Protect fields that should not be directly set via API requests
        read_only_fields = ['owner', 'created_at'] 


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    It includes read-only fields for context (listing title and guest username).
    """
    
    # Display the listing's title for context
    listing_title = serializers.ReadOnlyField(source='listing.title')
    
    # Display the guest's username for context
    guest_username = serializers.ReadOnlyField(source='guest.username')

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_title', 'guest', 'guest_username', 
            'check_in_date', 'check_out_date', 'total_price', 
            'is_confirmed', 'created_at'
        ]
        # Protect fields: 'total_price' should be calculated in the view/model logic,
        # 'is_confirmed' should be set by a business logic process, not the user.
        # 'guest' is often set automatically by the view (request.user).
        read_only_fields = ['total_price', 'is_confirmed', 'created_at']