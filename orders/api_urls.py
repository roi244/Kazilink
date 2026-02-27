from rest_framework.routers import DefaultRouter

from .api import MissionOrderViewSet

app_name = 'orders-api'

router = DefaultRouter()
router.register('missions', MissionOrderViewSet, basename='missions')

urlpatterns = router.urls
