from rest_framework import permissions, viewsets

from .models import ProviderService, ServiceCategory
from .serializers import ProviderServiceSerializer, ServiceCategorySerializer


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]


class ProviderServiceViewSet(viewsets.ModelViewSet):
    queryset = ProviderService.objects.select_related('provider', 'provider__profile', 'category').filter(is_active=True)
    serializer_class = ProviderServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)
