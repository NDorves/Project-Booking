from rest_framework.routers import DefaultRouter
from django.urls import path, include
from booking_app.reviews.views import ReviewViewSet

router = DefaultRouter()

router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
