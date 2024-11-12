from django.db import models
from django.utils import timezone

from booking_app.listings.models.model import Listings
from booking_app.user.models.model import User
from django.utils.translation import gettext_lazy as _


class BookingStatus(models.IntegerChoices):
    PENDING = 0, _('Pending')
    CONFIRMED = 1, _('Confirmed')
    REJECTED = 2, _('Rejected')
    CANCELLED = 3, _('Cancelled')


class Booking(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='bookings',
                                help_text='property type')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.IntegerField(choices=BookingStatus.choices, default=BookingStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.listing.title} ({self.start_date} to {self.end_date})'

    class Meta:
        ordering = ['-updated_at']

    def confirm(self, user):
        '''Подтверждение бронирования владельцем жилья.'''
        if user != self.listing.owner:
            raise PermissionError('Only the host can confirm the booking.')
        if self.status != BookingStatus.PENDING:
            raise ValueError('Only pending bookings can be confirmed.')
        self.status = BookingStatus.CONFIRMED
        self.save()

    def reject(self, user):
        '''Отклонение бронирования владельцем жилья.'''
        if user != self.listing.owner:
            raise PermissionError('Only the owner can reject the booking.')
        if self.status != BookingStatus.PENDING:
            raise ValueError('Only pending bookings can be rejected.')
        self.status = BookingStatus.REJECTED
        self.save()

    def cancel(self, user):
        '''Отмена бронирования арендатором.'''
        if user != self.user:
            raise PermissionError('Only the renter can cancel the booking.')
        if self.status != BookingStatus.CONFIRMED:
            raise ValueError('Only confirmed bookings can be cancelled.')
        if not self.is_cancelable():
            raise ValueError('It\'s too late to cancel this booking.')
        self.status = BookingStatus.CANCELLED
        self.save()

    def is_cancelable(self):
        '''Может ли арендатор отменить бронирование?'''
        days_to_start_date = (
            self.start_date - timezone.now().date()
        ).days
        return days_to_start_date >= 1




