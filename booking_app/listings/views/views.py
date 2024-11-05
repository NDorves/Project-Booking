from rest_framework import viewsets

from booking_app.listings.models.model import Listings
from booking_app.listings.serializers.listings_serializer import ListingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listings.objects.all()
    serializer_class = ListingSerializer
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['price', 'rooms', 'property_type', 'is_active', 'location']
    # search_fields = ['title', 'description']
    # ordering_fields = ['created_at', 'price', 'views']
    # permission_classes = [IsAuthenticated]
    #
    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsAdminUser]
    #     return super().get_permissions()
