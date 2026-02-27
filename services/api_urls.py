from rest_framework.routers import DefaultRouter

from .api import ProviderServiceViewSet, ServiceCategoryViewSet

app_name = 'services-api'

router = DefaultRouter()
router.register('categories', ServiceCategoryViewSet, basename='categories')
router.register('providers', ProviderServiceViewSet, basename='providers')

urlpatterns = router.urls
