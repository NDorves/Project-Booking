from django.db import models
from booking_app.listings.models.model import Listings
from booking_app.user.models.model import User
from django.core.validators import MaxValueValidator


class Review(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} = {self.listing.title}'
