from django.urls import path, include
from booking_app import views

urlpatterns = [
    path('', views.first_view, name='first'),
    path('', include('booking_app.booking.urls')),
    path('', include('booking_app.history.urls')),
    path('', include('booking_app.listings.urls')),
    path('', include('booking_app.reviews.urls')),
    path('', include('booking_app.user.urls')),


]
