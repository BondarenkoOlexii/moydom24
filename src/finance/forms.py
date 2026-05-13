from django import forms
from django.forms import inlineformset_factory

from src.finance.models import Payment_Account, Invoice, ThoughInvoiceService
from src.settings.models import Service, Tariff

class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = Payment_Account
        fields = ['bank_book', 'status', 'apartment']

        widgets = {
            'apartment': forms.Select(attrs={'id': 'flatform-flat_id', 'class': 'form-control'}),
            'bank_book': forms.TextInput(attrs={'id': 'account-uid', 'class': 'form-control'}),
            'status': forms.Select(attrs={'id': 'account-status', 'class': 'form-control'})
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['type', 'create_time', 'service', 'transaction', 'total_amount', 'payment_account', 'status',
                  'period_end', 'period_start', 'invoice_unique_id', 'tariff']

        widgets = {
            'invoice_unique_id': forms.TextInput(attrs={'id': 'invoice-uid', 'class': 'form-control'}),
            'create_time': forms.DateInput(attrs={'id': 'invoice-uid_date', 'class': 'form-control krajee-datepicker'}),
            'period_start': forms.DateInput(attrs={'id': 'invoice-period_start_date', 'class': 'form-control krajee-datepicker'}),
            'period_end': forms.DateInput(attrs={'id': 'invoice-period_end_date', 'class': 'form-control krajee-datepicker'}),


            'type': forms.Select(attrs={'id': 'invoice-status', 'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'id': 'invoice-is_checked', 'type': 'checkbox'}),
            'payment_account': forms.TextInput(attrs={'id': 'account_uid', 'class': 'form-control'}),
            'tariff': forms.Select(attrs={'id': 'invoice-tariff_id', 'class': 'form-control'})

        }

class InvoiceServiceForm(forms.ModelForm):
    class Meta:
        model = ThoughInvoiceService
        fields = ['service', 'indicator', 'price', 'measurement', 'measurement_price']

        widgets = {
            'service': forms.Select(attrs={'id': 'service-name', 'class': 'form-control'}),
            'indicator': forms.TextInput(attrs={'id': '', 'class': 'form-control'}),
            'price': forms.TextInput(attrs={'id': '', 'class': 'form-control'}),
            'measurement': forms.Select(attrs={'class': 'form-control'}),
            'measurement_price': forms.TextInput(attrs={'class': 'form-control'})
        }


InvoiceServiceFormSet = inlineformset_factory(Invoice, ThoughInvoiceService, InvoiceServiceForm, extra=0, can_delete=True)