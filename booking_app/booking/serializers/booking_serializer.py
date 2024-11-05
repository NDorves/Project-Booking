from rest_framework import serializers

from booking_app.booking.models.model import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
