from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.username', read_only=True)
    provider_username = serializers.CharField(source='provider.username', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'mission',
            'client',
            'client_username',
            'provider',
            'provider_username',
            'rating',
            'comment',
            'created_at',
        )
        read_only_fields = ('client', 'provider', 'created_at')
