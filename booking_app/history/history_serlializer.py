from typing import Any
from django.urls import reverse
from rest_framework import serializers
from booking_app.history.models import *


class ViewHistorySerializer(serializers.ModelSerializer):
    listing_str = serializers.SerializerMethodField()
    listing_url = serializers.SerializerMethodField()

    class Meta:
        model = ViewHistory
        exclude = ['id', 'user']

    def get_listing_str(self, obj) -> str:
        return f'{obj.listing.title} - {obj.listing.location}'

    def get_listing_url(self, obj) -> Any | None:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('listings-detail', kwargs={'pk': obj.listing.pk})
            )
        return None


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        exclude = ['id', 'user']


class SearchStatsSerializer(serializers.Serializer):
    term = serializers.CharField(max_length=255)
    total_searches = serializers.IntegerField()
