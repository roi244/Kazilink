from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('', views.home, name='home'),
    path('publier-service/', views.publish_service, name='publish_service'),
]
