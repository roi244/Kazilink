from django.contrib import admin

from .models import ProviderService, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProviderService)
class ProviderServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'category', 'city', 'is_active')
    list_filter = ('category', 'city', 'is_active')
    search_fields = ('title', 'provider__username', 'city')
