from rest_framework import serializers

from .models import ProviderService, ServiceCategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ('id', 'name', 'slug', 'description')


class ProviderServiceSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(source='provider.username', read_only=True)
    provider_city = serializers.CharField(source='provider.profile.city', read_only=True)
    provider_verified = serializers.BooleanField(source='provider.profile.is_verified', read_only=True)
    whatsapp_url = serializers.CharField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = ProviderService
        fields = (
            'id',
            'provider',
            'provider_city',
            'provider_verified',
            'category',
            'category_name',
            'title',
            'description',
            'city',
            'years_experience',
            'base_price',
            'whatsapp_url',
        )
