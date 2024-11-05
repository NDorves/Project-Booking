from rest_framework import serializers

from booking_app.listings.models.model import Listings


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listings
        fields = '__all__'