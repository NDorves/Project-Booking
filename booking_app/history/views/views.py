from django.db.models import Count
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from booking_app.history.serializers.history_serlializer import *


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    # permission_classes = [IsAuthenticated]
    # @extend_schema(summary="Получить историю поисковых запросов аутентифицированного пользователя")
    # @action(
    #     methods=['get'],
    #     detail=False,
    #     url_path='my-search-history',
    #     permission_classes=[permissions.IsAuthenticated]
    # )

    def my_search_history(self, request):
        search_history = SearchHistory.objects.filter(
            user=request.user
        ).order_by('-searched_at')
        search_history = [search for search in search_history]
        serializer = SearchHistorySerializer(search_history, many=True)
        return Response(serializer.data)

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


class ViewHistoryViewSet(viewsets.ModelViewSet):
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer
    # permission_classes = [IsAuthenticated]

    def my_view_history(self, request):
        view_history = ViewHistory.objects.filter(
            user=request.user
        ).order_by('-viewed_at')
        view_history = [view for view in view_history]
        serializer = ViewHistorySerializer(
            view_history, many=True, context={'request': request}
        )
        return Response(serializer.data)

