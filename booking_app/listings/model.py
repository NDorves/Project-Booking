from django.db import models

from booking_app.user.model import User

PROPERTY_CHOICES = [
        ('Room', 'Room'),
        ('Suite', 'Suite'),
        ('Studio', 'Studio'),
        ('Apartment', 'Apartment'),
        ('Hostel', 'Hostel'),
        ('House', 'House'),
        ('Villa', 'Villa'),
    ]
CATEGORY_CHOICES = [
    ('without category', 'without category'),
    ('3-stars', '3-stars'),
    ('4-stars', '4-stars'),
    ('5-stars', '5-stars'),
]


class Listings(models.Model):
    title = models.CharField(max_length=255, unique=True)
    category = models.SlugField(choices=CATEGORY_CHOICES, help_text='enter category star',
                                default='without category', null=True) #ввести категорию звезд, по умолчанию='без категории'
    image = models.ImageField(upload_to='poster_images/',
                              help_text='Upload image', null=True, blank=True)  #Загрузите изображение
    is_active = models.BooleanField(default=True)
    property_type = models.CharField(choices=PROPERTY_CHOICES, max_length=50, default='Room')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    location = models.CharField(max_length=250, help_text="Landmark (location)", verbose_name="Where is", null=True)
    site_link = models.URLField(max_length=150, unique=True,
                                help_text="Object page link (https://www.google.de/maps/",
                                verbose_name="Link to page", null=True)
    rooms = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(null=True, default=0)
    number_of_reviews = models.IntegerField(default=0)
    number_of_views = models.IntegerField(default=0)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,
                              related_name='owner_listings', null=True)
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

    class Meta:
        ordering = ['-updated_at']  # Сортировка по убыванию даты создания.
        verbose_name = 'Listings'  # Человекочитаемое имя модели: 'Listing'.
        # unique_together = ['title']  # Уникальность по полю 'title'.

    def update_views(self):
        '''
        Обновление счетчика просмотров объявления
        use in ListingViewSet.retrieve (listings.views.py)
        '''
        self.number_of_views = self.view_history.count()
        self.save()

    def update_rating(self):
        '''
        Обновление рейтинга и счетчика отзывов
        use in signals (reviews.signals.py):
            update_listing_rating_on_save
            update_listing_rating_on_delete
        '''
        reviews = self.reviews.aggregate(
            rating=models.Avg('rating'),
            number_of_reviews=models.Count('id')
        )
        self.rating = reviews['rating'] or 0.0
        self.number_of_reviews = reviews['number_of_reviews']
        self.save()