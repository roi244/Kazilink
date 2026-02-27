from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('ajouter/<int:mission_id>/', views.add_review, name='add_review'),
    path('prestataire/<int:provider_id>/', views.provider_reviews, name='provider_reviews'),
]
