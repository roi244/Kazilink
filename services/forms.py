from django import forms

from .models import ProviderService


class ProviderServiceForm(forms.ModelForm):
    class Meta:
        model = ProviderService
        fields = ('category', 'title', 'description', 'city', 'years_experience', 'base_price')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'base_price': 'Prix de base (FCFA)',
        }
        help_texts = {
            'base_price': 'La conversion en EUR est appliquee uniquement a l\'affichage.',
        }


class ServiceSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Recherche')
    city = forms.CharField(required=False, label='Ville')
    category = forms.CharField(required=False, label='Categorie')
