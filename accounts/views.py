from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, SignupForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('services:home')

    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Compte cree avec succes.')
        return redirect('services:home')

    return render(request, 'accounts/signup.html', {'form': form})


class KaziLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('services:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Connexion reussie.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Identifiants invalides, veuillez reessayer.')
        return super().form_invalid(form)

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'provider':
            return reverse_lazy('orders:my_orders')
        return reverse_lazy('services:home')


class KaziLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('services:home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Vous etes deconnecte.')
        return super().dispatch(request, *args, **kwargs)
