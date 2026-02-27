from rest_framework import serializers

from .models import MissionOrder


class MissionOrderSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.username', read_only=True)
    provider_username = serializers.CharField(source='provider_service.provider.username', read_only=True)
    service_title = serializers.CharField(source='provider_service.title', read_only=True)

    class Meta:
        model = MissionOrder
        fields = (
            'id',
            'client',
            'client_username',
            'provider_service',
            'provider_username',
            'service_title',
            'city',
            'address',
            'description',
            'preferred_date',
            'total_amount',
            'commission_amount',
            'status',
            'payment_status',
            'payment_provider',
            'payment_reference',
            'amount_paid',
            'paid_at',
            'created_at',
        )
        read_only_fields = (
            'client',
            'commission_amount',
            'status',
            'payment_status',
            'payment_provider',
            'payment_reference',
            'amount_paid',
            'paid_at',
            'created_at',
        )
