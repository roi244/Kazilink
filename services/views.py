from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from accounts.models import UserProfile

from .forms import ProviderServiceForm, ServiceSearchForm
from .models import ProviderService, ServiceCategory


def home(request):
    services_qs = ProviderService.objects.filter(is_active=True).select_related('provider', 'provider__profile', 'category')
    search_form = ServiceSearchForm(request.GET or None)

    if search_form.is_valid():
        q = search_form.cleaned_data.get('q')
        city = search_form.cleaned_data.get('city')
        category = search_form.cleaned_data.get('category')

        if q:
            services_qs = services_qs.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(provider__username__icontains=q)
            )
        if city:
            services_qs = services_qs.filter(city__icontains=city)
        if category:
            services_qs = services_qs.filter(category__slug=category)

    context = {
        'services': services_qs[:30],
        'categories': ServiceCategory.objects.filter(is_active=True),
        'search_form': search_form,
    }
    return render(request, 'services/home.html', context)


@login_required
def publish_service(request):
    profile = request.user.profile
    if profile.role != UserProfile.ROLE_PROVIDER:
        messages.error(request, 'Seuls les prestataires peuvent publier un service.')
        return redirect('services:home')

    form = ProviderServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        provider_service = form.save(commit=False)
        provider_service.provider = request.user
        provider_service.save()
        messages.success(request, 'Service publie avec succes.')
        return redirect('services:home')

    return render(request, 'services/publish_service.html', {'form': form})
