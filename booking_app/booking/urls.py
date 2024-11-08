from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking_app.booking.views.views import BookingViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
