from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from services.models import ProviderService


class MissionOrder(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'En attente'),
        (STATUS_ACCEPTED, 'Acceptee'),
        (STATUS_COMPLETED, 'Terminee'),
        (STATUS_CANCELLED, 'Annulee'),
    ]

    PAYMENT_UNPAID = 'unpaid'
    PAYMENT_REQUIRES_ACTION = 'requires_action'
    PAYMENT_PAID = 'paid'
    PAYMENT_FAILED = 'failed'
    PAYMENT_REFUNDED = 'refunded'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_UNPAID, 'Non paye'),
        (PAYMENT_REQUIRES_ACTION, 'Paiement en cours'),
        (PAYMENT_PAID, 'Paye'),
        (PAYMENT_FAILED, 'Paiement echoue'),
        (PAYMENT_REFUNDED, 'Rembourse'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_orders')
    provider_service = models.ForeignKey(ProviderService, on_delete=models.PROTECT, related_name='orders')
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    description = models.TextField()
    preferred_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_UNPAID)
    payment_provider = models.CharField(max_length=30, default='stripe', blank=True)
    payment_reference = models.CharField(max_length=255, blank=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_paid(self):
        return self.payment_status == self.PAYMENT_PAID

    def mark_paid(self, payment_reference='', amount=None):
        self.payment_status = self.PAYMENT_PAID
        self.payment_reference = payment_reference or self.payment_reference
        self.amount_paid = amount if amount is not None else self.total_amount
        self.paid_at = timezone.now()

    def save(self, *args, **kwargs):
        self.commission_amount = (self.total_amount or Decimal('0.00')) * Decimal('0.10')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Mission #{self.id} - {self.client.username}'
