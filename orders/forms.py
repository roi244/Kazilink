from django import forms

from .models import MissionOrder


class MissionRequestForm(forms.ModelForm):
    class Meta:
        model = MissionOrder
        fields = ('city', 'address', 'description', 'preferred_date', 'total_amount')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ManualPaymentProofForm(forms.Form):
    payment_reference = forms.CharField(
        max_length=255,
        label='Reference de paiement',
        help_text='Exemple: ID transaction Mobile Money, numero de recu, ou preuve WhatsApp.',
    )
