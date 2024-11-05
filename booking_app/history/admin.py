from django.contrib import admin

# Register your models here.
from booking_app.history.models.models import *

# Register your models here.
admin.site.register(SearchHistory),
admin.site.register(ViewHistory),
