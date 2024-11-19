from django.contrib import admin
from booking_app.history.models import ViewHistory, SearchHistory


@admin.register(ViewHistory)
class ViewHistoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(SearchHistory)
class LSearchHistoryModelAdmin(admin.ModelAdmin):
    pass
