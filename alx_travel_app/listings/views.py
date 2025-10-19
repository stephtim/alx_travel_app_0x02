from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

# Create your views here.
def home(request):
    return HttpResponse("<h1>Hello World!</h1>")

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
