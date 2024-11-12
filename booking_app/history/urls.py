from rest_framework.routers import DefaultRouter
from django.urls import path, include
from booking_app.history.views.views import *

router = DefaultRouter()
router.register(r'search-history', SearchHistoryViewSet)
router.register(r'view-history', ViewHistoryViewSet)
#router.register(r'search-form/', SearchHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
