from rest_framework.routers import DefaultRouter
from django.urls import path, include
from booking_app.listings.views.views import *

router = DefaultRouter()
router.register(r'listings', ListingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
