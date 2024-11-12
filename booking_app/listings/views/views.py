from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from booking_app.history.models.models import ViewHistory
from booking_app.listings.serializers.listings_serializer import *


class ListingViewSet(viewsets.ModelViewSet):
    view = Listings.objects.select_related('ViewHistory').select_related('SearchHistory')
    queryset = Listings.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'rooms', 'property_type', 'is_active']
    search_fields = ['title', 'description', 'property_type']
    ordering_fields = ['title', '-created_at', 'price', 'views']
    # permission_classes = [IsAuthenticated]
    #
    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsAdminUser]
    #     return super().get_permissions()

    @action(detail=False, methods=['get'])
    def statistic(self, request):
        view_counts = Listings.objects.annotate(view_count=Count('view'))
        data = [
            {
                "id": ViewHistory.listing,
                "view_count": ViewHistory.view_count
            }
            for view in view_counts
        ]
        return Response(data)



