from django.db import models
from booking_app.listings.models.model import Listings
from booking_app.user.models.model import User


class Booking(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.listing.title}'

from django.db import models

# Create your models here.
