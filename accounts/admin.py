from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'profession', 'city', 'is_verified')
    list_filter = ('role', 'is_verified', 'city')
    search_fields = ('user__username', 'profession', 'phone', 'whatsapp_number', 'city')
