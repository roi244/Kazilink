from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    phone = forms.CharField(required=False)
    city = forms.CharField(required=False)
    whatsapp_number = forms.CharField(required=False, label='Numero WhatsApp')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'phone',
            'city',
            'whatsapp_number',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.phone = self.cleaned_data['phone']
            profile.city = self.cleaned_data['city']
            profile.whatsapp_number = self.cleaned_data['whatsapp_number']
            profile.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nom utilisateur')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
