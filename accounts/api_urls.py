from rest_framework.routers import DefaultRouter

from .api import UserProfileViewSet

app_name = 'accounts-api'

router = DefaultRouter()
router.register('profiles', UserProfileViewSet, basename='profiles')

urlpatterns = router.urls
