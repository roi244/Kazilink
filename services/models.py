from django.conf import settings
from django.db import models
from django.utils.text import slugify


class ServiceCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Service categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProviderService(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='provided_services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='providers')
    title = models.CharField(max_length=150)
    description = models.TextField()
    city = models.CharField(max_length=120)
    years_experience = models.PositiveIntegerField(default=0)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('provider', 'category', 'title')

    def __str__(self):
        return f'{self.title} - {self.provider.username}'

    @property
    def whatsapp_url(self):
        number = getattr(self.provider.profile, 'whatsapp_number', '')
        if not number:
            return ''
        clean_number = ''.join(char for char in number if char.isdigit())
        if not clean_number:
            return ''
        return f'https://wa.me/{clean_number}'
