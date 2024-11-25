
from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('landlord', 'landlord'),
    ('tenant', 'tenant'),
    ]


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE,  related_name='profile')
    description = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES) #, null=True)

    def __str__(self):
        return self.user.username
