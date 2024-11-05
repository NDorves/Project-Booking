
from booking_app.user.views.views import UserListGenericView, RegisterUserGenericView
from django.urls import path


urlpatterns = [
    path('users/', UserListGenericView.as_view(), name='user-list'),
    path('users/register/', RegisterUserGenericView.as_view(), name='user-register'),
]
