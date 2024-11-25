from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from booking_app.booking.model import Booking, BookingStatus
from booking_app.booking.permissions import AllowListingOwnerOrBookingUser, ReadOnly
from booking_app.booking.booking_serializer import BookingSerializer, ChoicesSerializer


class PropertyTypeListView(generics.ListAPIView):
    queryset = BookingStatus.choices
    serializer_class = ChoicesSerializer
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['results_label'] = 'results'
        return context

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            self.get_serializer_context()['results_label']: response.data
        }
        return response


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):     #Получить список всех бронирований аутентифицированного пользователя
        if self.action == 'list':
            return Booking.objects.filter(user=self.request.user)
        return Booking.objects.all()       #Получить детальную информацию о бронировании

    def get_permissions(self):      #Создать новое бронирование
        if self.action in ['create', 'my_hosted']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['confirm', 'reject', 'cancel']:
            return [AllowListingOwnerOrBookingUser()]
        else:
            return [AllowListingOwnerOrBookingUser(), ReadOnly()]

    def perform_create(self, serializer):       #Частично обновить бронирование,Удалить бронирование
        listing = serializer.validated_data['listing']
        current_price = listing.price
        serializer.save(user=self.request.user, price=current_price)

    @action(methods=['get'], detail=False, url_path='my-hosted')
    def my_hosted(self, request):
        queryset = Booking.objects.filter(listing__owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # "Подтвердить бронирование арендодателем"
    @action(methods=['post'], detail=True, url_path='confirm')
    def confirm(self, request, pk=None):
        booking = self.get_object()
        try:
            booking.confirm(request.user)
            return Response({"status": "confirmed"}, status=200)
        except PermissionError as e:
            raise PermissionDenied(str(e))
        except ValueError as e:
            raise ValidationError(str(e))

    # "Отклонить бронирование арендодателем")
    @action(methods=['post'], detail=True, url_path='reject')
    def reject(self, request, pk=None):
        booking = self.get_object()
        try:
            booking.reject(request.user)
            return Response({"status": "rejected"}, status=200)
        except PermissionError as e:
            raise PermissionDenied(str(e))
        except ValueError as e:
            raise ValidationError(str(e))

    #"Отменить бронирование арендатором")
    @action(methods=['post'], detail=True, url_path='cancel')
    def cancel(self, request, pk=None):
        booking = self.get_object()
        try:
            booking.cancel(request.user)
            return Response({"status": "cancelled"}, status=200)
        except PermissionError as e:
            raise PermissionDenied(str(e))
        except ValueError as e:
            raise ValidationError(str(e))

    @action(
        methods=['get'],
        detail=False,
        url_path='booking-statuses',
        permission_classes=[permissions.AllowAny]
    )
    def booking_statuses(self, request):
        queryset = BookingStatus.choices
        serializer = ChoicesSerializer(queryset, many=True)
        return Response({'results': serializer.data})



