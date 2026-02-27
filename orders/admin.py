from django.contrib import admin

from .models import MissionOrder


@admin.register(MissionOrder)
class MissionOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'provider_service',
        'status',
        'payment_status',
        'total_amount',
        'amount_paid',
        'commission_amount',
        'paid_at',
        'created_at',
    )
    list_filter = ('status', 'payment_status', 'city', 'created_at')
    search_fields = ('client__username', 'provider_service__title', 'city', 'payment_reference')
