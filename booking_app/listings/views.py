from datetime import timedelta
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from booking_app.booking.model import Booking, BookingStatus
from booking_app.history.models import ViewHistory, SearchHistory
from booking_app.history.history_serlializer import SearchStatsSerializer
from booking_app.listings.filters import CustomSearchFilter
from booking_app.listings.permissions import IsOwnerOrReadOnly
from booking_app.listings.listings_serializer import *
from booking_app.reviews.review_serializer import ReviewSerializer


# class ListingViewSet(viewsets.ModelViewSet):
#     view = Listings.objects.select_related('ViewHistory').select_related('SearchHistory')
#     queryset = Listings.objects.all()
#     serializer_class = ListingSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['price', 'rooms', 'property_type', 'is_active']
#     search_fields = ['title', 'description', 'property_type']
#     ordering_fields = ['title', '-created_at', 'price', 'views']
#     # permission_classes = [IsAuthenticated]
#     #
#     # def get_permissions(self):
#     #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
#     #         self.permission_classes = [IsAdminUser]
#     #     return super().get_permissions()
#
#     @action(detail=False, methods=['get'])
#     def statistic(self, request):
#         view_counts = Listings.objects.annotate(view_count=Count('view'))
#         data = [
#             {
#                 "id": ViewHistory.listing,
#                 "view_count": ViewHistory.view_count
#             }
#             for view in view_counts
#         ]
#         return Response(data)
#
#
#
# class PropertyTypeListView(generics.ListAPIView):
#     queryset = PropertyType.choices
#     serializer_class = ChoicesSerializer
#     pagination_class = None
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['results_label'] = 'results'
#         return context
#
#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         response.data = {
#             self.get_serializer_context()['results_label']: response.data
#         }
#         return response


# @extend_schema_view(
#     list=extend_schema(summary="Получить список всех активных объявлений", responses={},),
#     create=extend_schema(summary="Создать новое объявление",),
#     retrieve=extend_schema(summary="Получить детальную информацию об объявления",),
#     update=extend_schema(summary="Обновить объявление",),
#     partial_update=extend_schema(summary="Частично обновить объявление",),
#     destroy=extend_schema(summary="Удалить объявление",),
# )  # https://habr.com/ru/articles/733942/

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

    # @extend_schema(summary="Получить список объявлений созданных аутентифицированным пользователем")
    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path='my-created',
    #     permission_classes=[permissions.IsAuthenticated]
    # )
    def my_created(self, request):
        queryset = Listings.objects.filter(owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # @extend_schema(summary="Получить историю просмотренных объявлений аутентифицированного пользователя")
    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path='my-view-history',
    #     permission_classes=[permissions.IsAuthenticated]
    # )
    # def my_view_history(self, request):
    #     view_history = ViewHistory.objects.filter(
    #         user=request.user
    #     ).order_by('-viewed_at')
    #     view_history = [view for view in view_history]
    #     serializer = ViewHistorySerializer(
    #         view_history, many=True, context={'request': request}
    #     )
    #     return Response(serializer.data)

    # @extend_schema(summary="Получить историю поисковых запросов аутентифицированного пользователя")
    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path='my-search-history',
    #     permission_classes=[permissions.IsAuthenticated]
    # )
    # def my_search_history(self, request):
    #     search_history = SearchHistory.objects.filter(
    #         user=request.user
    #     ).order_by('-searched_at')
    #     search_history = [search for search in search_history]
    #     serializer = SearchHistorySerializer(search_history, many=True)
    #     return Response(serializer.data)

    # @extend_schema(summary="Получить список популярных поисковых запросов")
    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path='search-stats',
    #     permission_classes=[permissions.IsAuthenticated]
    # )
    def search_stats(self, request):
        search_stats = (
            SearchHistory.objects
            .values('term')
            .annotate(total_searches=Count('term'))
            .order_by('-total_searches')
        )
        search_stats = [search for search in search_stats]
        serializer = SearchStatsSerializer(search_stats, many=True)
        return Response(serializer.data)

    # @extend_schema(summary="Получить список забронированых периодов для объявления")
    # @action(
    #     methods=['get'],
    #     detail=True,
    #     url_path='reserved-periods',
    #     permission_classes=[permissions.AllowAny]
    # )
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

    # @extend_schema(summary="Получить список забронированых дат для объявления")
    # @action(
    #     methods=['get'],
    #     detail=True,
    #     url_path='reserved-dates',
    #     permission_classes=[permissions.AllowAny]
    # )
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

    # @extend_schema(summary="Получить список отзывов для объявления")
    # @action(
    #     methods=['get'],
    #     detail=True,
    #     url_path='reviews',
    #     permission_classes=[permissions.AllowAny]
    # )
    def reviews(self, request, pk=None):
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request}
        )
        return Response(serializer.data)

    # @extend_schema(summary="Получить виды недвижимости с их кодами")
    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path='property-types',
    #     permission_classes=[permissions.AllowAny]
    # )
    # def property_types(self, request):
    #     queryset = PropertyType.choices
    #     serializer = ChoicesSerializer(queryset, many=True)
    #     return Response({'results': serializer.data})