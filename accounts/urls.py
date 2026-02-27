from django.urls import path

from .views import KaziLoginView, KaziLogoutView, signup_view

app_name = 'accounts'

urlpatterns = [
    path('inscription/', signup_view, name='signup'),
    path('connexion/', KaziLoginView.as_view(), name='login'),
    path('deconnexion/', KaziLogoutView.as_view(), name='logout'),
]
