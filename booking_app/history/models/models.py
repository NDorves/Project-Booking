from django.db import models
from booking_app.listings.models.model import Listings
from booking_app.user.models.model import User
SEARCH_CHOICES = [
        ('Room', 'Room'),
        ('Suite', 'Suite'),
        ('Studio', 'Studio'),
        ('Apartment', 'Apartment'),
        ('Hostel', 'Hostel'),
        ('House', 'House'),
        ('Villa', 'Villa'),


    ]


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50, choices=SEARCH_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, related_name='search_listings')
#    location = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, related_query_name='listings.location')


class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null=True, related_name='listings_view')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.listing.title}'



