from rest_framework import viewsets

from booking_app.reviews.models.model import Review
from booking_app.reviews.serializers.review_serializer import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
