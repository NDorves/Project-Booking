from django.shortcuts import render
from rest_framework import viewsets
from booking_app.history.serializers.history_serlializer import *


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    # permission_classes = [IsAuthenticated]

    def search_view(request):
        form = SearchForm()
        results = []
        if request.method == 'GET':
            form = SearchForm(request.GET)
            if form.is_valid():
                keywords = form.cleaned_data.get('keywords')
                min_price = form.cleaned_data.get('min_price')
                max_price = form.cleaned_data.get('max_price')
                location = form.cleaned_data.get('location')
                min_rooms = form.cleaned_data.get('min_rooms')
                max_rooms = form.cleaned_data.get('max_rooms')
                property_type = form.cleaned_data.get('property_type')
                sort_by = form.cleaned_data.get('sort_by')
                order = form.cleaned_data.get('order')
                query = Listings.objects.all()
                if keywords:
                    keyword_list = [kw.strip() for kw in keywords.split(',')]
                    for keyword in keyword_list:
                        query = query.filter(models.Q(title__icontains=keyword) | models.Q(description__icontains=keyword))
                if min_price is not None:
                    query = query.filter(price__gte=min_price)
                if max_price is not None:
                    query = query.filter(price__lte=max_price)
                if location:
                    query = query.filter(location__icontains=location)
                if min_rooms is not None:
                    query = query.filter(rooms__gte=min_rooms)
                if max_rooms is not None:
                    query = query.filter(rooms__lte=max_rooms)
                if property_type:
                    query = query.filter(property_type=property_type)
                if sort_by:
                    if order == 'desc':
                        sort_by = f'-{sort_by}'
                    query = query.order_by(sort_by)
                    results = query
                    # Save search history
                if request.user.is_authenticated:
                    for keyword in keyword_list:
                        SearchHistory.objects.create(user=request.user, keyword=keyword, listing=None)
        return render(request, 'search.html', {'form': form, 'results': results})


class ViewHistoryViewSet(viewsets.ModelViewSet):
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer
    # permission_classes = [IsAuthenticated]



