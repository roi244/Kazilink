from rest_framework import permissions, viewsets

from .models import MissionOrder
from .serializers import MissionOrderSerializer


class MissionOrderViewSet(viewsets.ModelViewSet):
    serializer_class = MissionOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MissionOrder.objects.filter(client=user).select_related('provider_service', 'provider_service__provider')

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
