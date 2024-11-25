from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking_app.booking.views import BookingViewSet
from booking_app.listings.views import ListingViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'listings', ListingViewSet, basename='listing')


urlpatterns = [
    path('', include(router.urls)),
]
