from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers

from booking_app.booking.models.model import Booking, BookingStatus
from booking_app.user.serializers.user_serializer import UserListSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    status_display = serializers.SerializerMethodField()
    booking_url = serializers.SerializerMethodField()
    listing_url = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'

        read_only_fields = [
            'user', 'price', 'status', 'created_at', 'updated_at'
        ]

    def get_status_display(self, obj) -> str:
        return obj.get_status_display()

    def get_booking_url(self, obj) -> str:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('booking-detail', kwargs={'pk': obj.pk})
            )
        return None

    def get_listing_url(self, obj) -> str:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('listing-detail', kwargs={'pk': obj.listing.pk})
            )
        return None

    def validate(self, data):
        listing = data.get('listing')
        if not listing.is_active:
            raise serializers.ValidationError(
                'It is not possible to book an inactive listing.'
            )
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date < timezone.now().date():
            raise serializers.ValidationError(
                'The booking start date cannot be in the past.'
            )
        if start_date >= end_date:
            raise serializers.ValidationError(
                'The start date of the booking must be before the end date.'
            )
        overlapping_bookings = Booking.objects.filter(
            listing=listing,
            status=BookingStatus.CONFIRMED
        ).filter(
            Q(start_date__lt=end_date)
            & Q(end_date__gt=start_date)
        )
        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                'The selected dates overlap with existing bookings.'
            )
        return data
