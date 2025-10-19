from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, home
from .views import initiate_payment, verify_payment, chapa_callback
from .views import create_booking_and_payment, chapa_callback

urlpatterns = [
    path('booking/create-payment/', create_booking_and_payment, name='create_booking_and_payment'),
    path('payment/callback/', chapa_callback, name='chapa_callback'),
]

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', home),
    path('api/', include(router.urls)),
]

urlpatterns = [
    path('initiate-payment/', initiate_payment, name='initiate_payment'),
    path('verify-payment/<str:tx_ref>/', verify_payment, name='verify_payment'),
]

urlpatterns = [
    path('initiate-payment/', initiate_payment, name='initiate_payment'),
    path('verify-payment/<str:tx_ref>/', verify_payment, name='verify_payment'),
    path('payment/callback/', chapa_callback, name='chapa_callback'),
]