from rest_framework.routers import DefaultRouter

from .api import ReviewViewSet

app_name = 'reviews-api'

router = DefaultRouter()
router.register('', ReviewViewSet, basename='reviews')

urlpatterns = router.urls
