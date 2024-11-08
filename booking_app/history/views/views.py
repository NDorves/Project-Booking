from rest_framework import viewsets
from booking_app.history.serializers.history_serlializer import *


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    # permission_classes = [IsAuthenticated]


class ViewHistoryViewSet(viewsets.ModelViewSet):
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer
    # permission_classes = [IsAuthenticated]



