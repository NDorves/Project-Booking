from django.db import models
from booking_app.listings.models.model import Listings
from booking_app.user.models.model import User


class Booking(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='listing',
                                help_text='property type')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(unique_for_date='start_date')
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    booking = models.DateTimeField(auto_now_add=True, help_text='Время создания записи', null=True)

    def __str__(self):
        return f'{self.user.username} - {self.listing.title}'


