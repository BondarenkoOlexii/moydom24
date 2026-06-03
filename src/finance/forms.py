from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from src.finance.models import Payment_Account, Invoice, ThoughInvoiceService, Cash_Register
from src.settings.models import Service, Tariff
from src.users.models import User
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


class CashRegisterForm(forms.ModelForm):

    apartment = forms.ModelChoiceField(queryset=User.objects.all(),
                                       widget=s2forms.Select2Widget(attrs={'id': 'w1', 'class': 'form-control'}),
                                       required=False)

    class Meta:
        model = Cash_Register
        fields = ['unique_id', 'create_time', 'status', 'sum', 'comment', 'article', 'account', 'manager']

        widgets = {
            'unique_id': forms.TextInput(attrs={'id': 'accounttransaction-uid', 'class': 'form-control'}),
            'create_time': forms.DateInput(attrs={'id': 'accounttransaction-uid_date', 'class': 'form-control krajee-datepicker'}),
            'status': forms.CheckboxInput(attrs={'id': 'is_complete'}),
            'sum': forms.TextInput(attrs={'id': 'accounttransaction-amount', 'class': 'form-control'}),
            'article': forms.TextInput(attrs={'id': 'accounttransaction-transaction_purpose_id', 'class': 'form-control'}),
            'manager': forms.Select(attrs={'id': 'accounttransaction-user_admin_id', 'class': 'form-control'}),
            'account': forms.Select(attrs={'id': 'accounttransaction-payment_account', 'class': 'form-control'}),
        }