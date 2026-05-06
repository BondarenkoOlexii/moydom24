from django import forms

from src.finance.models import Payment_Account

class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = Payment_Account
        fields = ['bank_book', 'status', 'apartment']

        widgets = {
            'apartment': forms.Select(attrs={'id': 'flatform-flat_id', 'class': 'form-control'}),
            'bank_book': forms.TextInput(attrs={'id': 'account-uid', 'class': 'form-control'}),
            'status': forms.Select(attrs={'id': 'account-status', 'class': 'form-control'})
        }