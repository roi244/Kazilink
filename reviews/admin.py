from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission', 'client', 'provider', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('client__username', 'provider__username', 'mission__id')
