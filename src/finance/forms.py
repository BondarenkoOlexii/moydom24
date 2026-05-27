from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

from src.finance.models import Payment_Account, Invoice, ThoughInvoiceService
from src.settings.models import Service, Tariff

class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = Payment_Account
        fields = ['bank_book', 'status', 'apartment']

        widgets = {
            'apartment': forms.Select(attrs={'id': 'flatform-apartment_id', 'class': 'form-control'}),
            'bank_book': forms.TextInput(attrs={'id': 'account-uid', 'class': 'form-control'}),
            'status': forms.Select(attrs={'id': 'account-status', 'class': 'form-control'})
        }

class InvoiceForm(forms.ModelForm):
    payment_account = forms.CharField(widget=forms.TextInput(attrs={'id': 'account_uid', 'class': 'form-control'}))


    class Meta:
        model = Invoice
        fields = ['type', 'create_time', 'status', 'period_end', 'period_start', 'invoice_unique_id', 'tariff', 'payment_account', 'total_amount']

        widgets = {
            'invoice_unique_id': forms.TextInput(attrs={'id': 'invoice-uid', 'class': 'form-control'}),
            'create_time': forms.DateInput(attrs={'id': 'invoice-uid_date', 'class': 'form-control krajee-datepicker'}),
            'period_start': forms.DateInput(attrs={'id': 'invoice-period_start_date', 'class': 'form-control krajee-datepicker'}),
            'period_end': forms.DateInput(attrs={'id': 'invoice-period_end_date', 'class': 'form-control krajee-datepicker'}),


            'type': forms.Select(attrs={'id': 'invoice-status', 'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'id': 'invoice-is_checked', 'type': 'checkbox'}),
            'tariff': forms.Select(attrs={'id': 'invoice-tariff_id', 'class': 'form-control'}),
            'total_amount': forms.TextInput(attrs={'id': 'invoice-total_amount', 'name': 'invoice-total_amount', 'type': 'hidden'})

        }

    def clean_payment_account(self):
        bank_book = self.cleaned_data.get('payment_account')
        try:
            account = Payment_Account.objects.get(bank_book=bank_book)
            return account
        except Payment_Account.DoesNotExist:
            raise forms.ValidationError("Payment Account does not exist", code='invalid_account')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.payment_account.bank_book:
            self.initial['payment_account'] = self.instance.payment_account.bank_book



class InvoiceServiceForm(forms.ModelForm):
    class Meta:
        model = ThoughInvoiceService
        fields = ['id','service', 'indicator', 'price', 'measurement', 'measurement_price']

        widgets = {
            'service': forms.Select(attrs={'id': 'service-name', 'class': 'form-control'}),
            'indicator': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'measurement': forms.Select(attrs={'class': 'form-control'}),
            'measurement_price': forms.TextInput(attrs={'class': 'form-control'})
        }


InvoiceServiceFormSet = inlineformset_factory(Invoice, ThoughInvoiceService, InvoiceServiceForm, extra=0, can_delete=True)