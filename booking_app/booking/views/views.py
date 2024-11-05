from rest_framework import viewsets

from booking_app.booking.models.model import Booking
from booking_app.booking.serializers.booking_serializer import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = [IsAuthenticated]

