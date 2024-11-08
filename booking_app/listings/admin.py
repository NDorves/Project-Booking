from django.contrib import admin

from booking_app.listings.models.model import Listings, Location

# Register your models here.
admin.site.register(Listings)
admin.site.register(Location)

