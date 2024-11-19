from django.contrib import admin
from booking_app.reviews.model import Review


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    pass
