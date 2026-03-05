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
    profession = forms.CharField(required=False, label='Metier / Specialite')
    bio = forms.CharField(
        required=False,
        label='Description de vos fonctions',
        widget=forms.Textarea(attrs={'rows': 4}),
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'phone',
            'city',
            'whatsapp_number',
            'profession',
            'bio',
            'password1',
            'password2',
        )

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        profession = (cleaned_data.get('profession') or '').strip()
        bio = (cleaned_data.get('bio') or '').strip()

        if role == UserProfile.ROLE_PROVIDER:
            if not profession:
                self.add_error('profession', 'Ce champ est obligatoire pour un prestataire.')
            if not bio:
                self.add_error('bio', 'Ce champ est obligatoire pour un prestataire.')

        cleaned_data['profession'] = profession
        cleaned_data['bio'] = bio
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.phone = self.cleaned_data['phone']
            profile.city = self.cleaned_data['city']
            profile.whatsapp_number = self.cleaned_data['whatsapp_number']
            profile.profession = self.cleaned_data['profession']
            profile.bio = self.cleaned_data['bio']
            profile.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nom utilisateur')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
