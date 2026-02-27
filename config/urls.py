from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('missions/', include('orders.urls')),
    path('avis/', include('reviews.urls')),
    path('', include('services.urls')),
    path('api/accounts/', include('accounts.api_urls')),
    path('api/services/', include('services.api_urls')),
    path('api/orders/', include('orders.api_urls')),
    path('api/reviews/', include('reviews.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
