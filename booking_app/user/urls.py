from django.urls import path, include
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter

from booking_app.user.views import UserViewSet, RegisterView, LoginView, LogoutView, EmailTokenObtainPairView

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path(
        'token/',
        views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),  # by username
    path(
        'token/refresh/',
        views.TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'token/',
        EmailTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),  # by e-mail

    # path('protected/', ProtectedView.as_view(), name='protected'),

    path('', include(router.urls)),
]


