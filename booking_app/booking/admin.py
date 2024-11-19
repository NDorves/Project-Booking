from django.contrib import admin

from booking_app.booking.model import Booking


@admin.register(Booking)
class BookingModelAdmin(admin.ModelAdmin):
    pass
