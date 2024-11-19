from typing import Any
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from rest_framework import serializers
from booking_app.booking.model import Booking, BookingStatus
from booking_app.user.user_serializer import UserSerializer


class ChoicesSerializer(serializers.Serializer):
    value = serializers.CharField()
    display_name = serializers.CharField()

    def to_representation(self, instance):
        return {'value': instance[0], 'display_name': instance[1]}


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
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

    def get_booking_url(self, obj) -> Any | None:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('booking-detail', kwargs={'pk': obj.pk}))
        return None

    def get_listing_url(self, obj) -> Any | None:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri({'pk': obj.listing.pk})
        #         reverse('listing-detail', kwargs=)
        # return None

    def validate(self, data):
        listing = data.get('listing')
        if not listing.is_active:
            raise serializers.ValidationError(
                'It is not possible to book an inactive listing.'  #Невозможно забронировать неактивное объявление.
            )
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date < timezone.now().date():
            raise serializers.ValidationError(
                'The booking start date cannot be in the past.'  #Дата начала бронирования не может быть в прошлом.
            )
        if start_date >= end_date:
            raise serializers.ValidationError(
                'The start date of the booking must be before the end date.'  #Дата нач.брон-я должна быть<даты оконч.
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
                'The selected dates overlap with existing bookings.'  #Выбранные даты совпадают с существ. бронир-ми.
            )
        return data
