from django import forms
from django.db import models
from booking_app.listings.models.model import Listings
from booking_app.user.models.model import User


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    term = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.term}'

    class Meta:
        ordering = ['-searched_at']


class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='view_history')
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, related_name='view_history')
    viewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} viewed {self.listing.title}'

    class Meta:
        ordering = ['-viewed_at']





