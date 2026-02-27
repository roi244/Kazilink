from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('nouvelle/<int:service_id>/', views.create_order, name='create_order'),
    path('mes-missions/', views.my_orders, name='my_orders'),
    path('status/<int:order_id>/<str:status>/', views.update_status, name='update_status'),
    path('paiement/<int:order_id>/checkout/', views.start_checkout, name='start_checkout'),
    path('paiement/<int:order_id>/manuel/', views.manual_payment, name='manual_payment'),
    path('paiement/<int:order_id>/valider-manuel/', views.confirm_manual_payment, name='confirm_manual_payment'),
    path('paiement/<int:order_id>/succes/', views.payment_success, name='payment_success'),
    path('paiement/<int:order_id>/annule/', views.payment_cancel, name='payment_cancel'),
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
