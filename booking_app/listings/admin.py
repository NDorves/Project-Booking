from django.contrib import admin
from booking_app.listings.model import Listings


@admin.register(Listings)
class ListingModelAdmin(admin.ModelAdmin):
    pass


