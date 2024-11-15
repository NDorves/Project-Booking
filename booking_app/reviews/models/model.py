from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from booking_app.listings.models.model import Listings
from booking_app.user.models.model import User


class Review(models.Model):
    RATING_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Very good', 'Very good'),
        ('Good', 'Good'),
        ('Sufficient', 'Sufficient')
    ]
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating_designation = models.CharField(max_length=50, choices=RATING_CHOICES, null=True)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                        MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.listing.title}'

    class Meta:
        ordering = ['-updated_at']

