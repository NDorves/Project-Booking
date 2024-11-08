from django.db import models


PROPERTY_CHOICES = [
        ('Room', 'Room'),
        ('Suite', 'Suite'),
        ('Studio', 'Studio'),
        ('Apartment', 'Apartment'),
        ('Hostel', 'Hostel'),
        ('House', 'House'),
        ('Villa', 'Villa'),
    ]


class Location(models.Model):
    city_name = models.CharField(max_length=50, null=True)
    street = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.city_name


class Listings(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='poster_images/', help_text='Загрузите изображение', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    property_type = models.CharField(choices=PROPERTY_CHOICES, max_length=50, default='Room')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    locations = models.ForeignKey(Location, on_delete=models.PROTECT, null=True, related_name='locations')
    rooms = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(auto_created=True, default=0)
    parking = models.BooleanField(default=False, null=True)
    pets_allowed = models.BooleanField(default=False, null=True)
    room_service = models.BooleanField(default=False, null=True)
    all_time_reception = models.BooleanField(default=False, null=True)
    wifi_included = models.BooleanField(default=False, null=True)
    wheelchair_accessible = models.BooleanField(default=False, null=True)
    pool = models.BooleanField(default=False, null=True)
    non_smoking_rooms = models.BooleanField(default=False, null=True)
    airport_shuttle = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title


