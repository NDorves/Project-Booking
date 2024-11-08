from rest_framework import serializers

from booking_app.listings.models.model import *


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listings
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

