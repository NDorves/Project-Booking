from rest_framework import serializers

from booking_app.reviews.models.model import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
