from rest_framework import viewsets, permissions
from booking_app.reviews.model import Review
from booking_app.reviews.permissions import IsOwnerOrReadOnly
from booking_app.reviews.review_serializer import ReviewSerializer


#Получить список всех отзывов аутентифицированного пользователя"
#Создать новый отзыв"
#Получить детальную информацию об отзыве"
#Обновить отзыв"
#Частично обновить отзыв"
#Удалить отзыв"

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return Review.objects.filter(user=self.request.user)
        return Review.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['create']:
            return [permissions.IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
