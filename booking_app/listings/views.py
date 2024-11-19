from datetime import timedelta
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from booking_app.booking.model import Booking, BookingStatus
from booking_app.history.models import ViewHistory, SearchHistory
from booking_app.history.history_serlializer import SearchStatsSerializer
from booking_app.listings.filters import CustomSearchFilter
from booking_app.listings.permissions import IsOwnerOrReadOnly
from booking_app.listings.listings_serializer import *
from booking_app.reviews.review_serializer import ReviewSerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listings.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        # filters.SearchFilter,
        CustomSearchFilter,
        filters.OrderingFilter
    ]

    #возможность указать мин/макс. цену,диапазон количества комнат,Тип жилья,Местоположение
    filterset_fields = {
        'price': ['lte', 'gte'],
        'rooms': ['range'],
        'location': ['icontains'],
        'parking': ['exact'],
        'room_service': ['exact'],
        'all_time_reception': ['exact'],
        'wifi_included': ['exact'],
        'wheelchair_accessible': ['exact'],
        'pool': ['exact'],
        'non_smoking_rooms': ['exact'],
        'airport_shuttle': ['exact'],
        # # 'property_typ': ['exact']
    }
    # Пользователь вводит ключевые слова, по которым производится поиск
    # в заголовках и описаниях объявлений
    search_fields = ['title', 'description', 'property_type', 'location']
    # Возможность сортировки по цене (возрастание/убывание),
    # дате добавления (новые/старые)
    ordering_fields = [
        'price',
        'created_at',
        'rating',
        'number_of_reviews',
        'number_of_views'

    ]
    ordering = ['id']

    def get_queryset(self):
        if self.action == 'list':
            return Listings.objects.filter(is_active=True)
        return Listings.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Запрет на просмотр неактивных объявлений, если это не владелец
        if not instance.is_active and instance.owner != request.user:
            raise PermissionDenied()
        # Если это не владелец, записываем просмотр
        if request.user.is_authenticated and instance.owner != request.user:
            ViewHistory.objects.update_or_create(
                listing=instance,
                user=request.user
            )
            instance.update_views()
        return super().retrieve(request, *args, **kwargs)

    # "Получить список объявлений созданных аутентифицированным пользователем")
    @action(
        methods=['get'],
        detail=False,
        url_path='my-created',
        permission_classes=[permissions.IsAuthenticated]
    )
    def my_created(self, request):
        queryset = Listings.objects.filter(owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def reserved_periods(self, request, pk=None):
        listing = self.get_object()
        bookings = Booking.objects.filter(
            listing=listing,
            status=BookingStatus.CONFIRMED
        ).values('start_date', 'end_date')
        reserved_dates = [
            {
                'check_in': booking['start_date'],
                'check_out': booking['end_date']
            }
            for booking in bookings
        ]
        return Response(reserved_dates)

    # "Получить список забронированых дат для объявления")
    @action(
        methods=['get'],
        detail=True,
        url_path='reserved-dates',
        permission_classes=[permissions.AllowAny]
    )
    def reserved_dates(self, request, pk=None):
        listing = self.get_object()
        bookings = Booking.objects.filter(
            listing=listing,
            status=BookingStatus.CONFIRMED
        ).values('start_date', 'end_date')
        reserved_dates = set()
        for booking in bookings:
            start_date = booking['start_date']
            end_date = booking['end_date']
            current_date = start_date
            while current_date <= end_date:
                reserved_dates.add(current_date)
                current_date += timedelta(days=1)
        reserved_dates = sorted(list(reserved_dates))
        return Response(reserved_dates)

    # "Получить список отзывов для объявления")
    @action(
        methods=['get'],
        detail=True,
        url_path='reviews',
        permission_classes=[permissions.AllowAny]
    )
    def reviews(self, request, pk=None):
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request}
        )
        return Response(serializer.data)

