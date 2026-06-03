from django import forms
from src.houses.models import Call_Master
from django.contrib.auth.forms import AuthenticationForm

class CabinetCallMaster(forms.ModelForm):
    class Meta:
        model = Call_Master
        fields = ['apartment', 'сonvenient_time', 'data_create', 'role', 'description', 'status']

        widgets = {
            'user': forms.Select(attrs={'type': 'hidden'}),
            'apartment': forms.Select(attrs={'id': 'masterrequest-flat_id-container', 'class': 'form-control'}),
            'data_create': forms.DateInput(attrs={'id': 'masterrequest-date_request', 'class': 'form-control krajee-datepicker', 'name': 'MasterRequest[date_request]','data-datepicker-source': 'masterrequest-date_request-kvdate', 'data-datepicker-type': '3','data-krajee-kvdatepicker': 'kvDatepicker_1643d6f1'}),
            'сonvenient_time': forms.TimeInput(attrs={'id': 'masterrequest-time_request', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'masterrequest-description', 'class': 'compose-textarea form-control', 'rows': '6','placeholder': 'Текст сообщения'}),
            'status': forms.Select(attrs={'id': 'masterrequest-status', 'class': 'form-control'}),
            'role': forms.Select(attrs={'id': 'masterrequest-type', 'class': 'form-control', 'value': ''}),
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label="Пароль", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    remember_me = forms.BooleanField(required=False, label='Запомнить меня', widget=forms.CheckboxInput(attrs={'class': 'icheckbox_flat-blue checked', 'style': 'position: relative;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'cabinet' in self.request.path:
            self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email или ID'})


class PaymentMethodChoise(forms.Form):
    card_number = forms.CharField(label='Номер карти', widget=forms.TextInput(attrs={'id': 'cardNumber', 'class': 'form-control form-shadow-sm', 'placeholder': 'XXXX XXXX XXXX XXXX', 'maxlength': '16'}))
    month = forms.CharField(label='Місяць', widget=forms.TextInput(attrs={'id': 'expMonth', 'class': 'form-control form-shadow-sm', 'placeholder': '05', 'maxlength': '2'}))
    year = forms.CharField(label='Рік', widget=forms.TextInput(attrs={'id': 'expYear', 'class': 'form-control form-shadow-sm', 'placeholder': '22', 'maxlength': '2'}))
    cvv = forms.CharField(label='CVV', widget=forms.TextInput(attrs={'class': 'form-control form-shadow-sm w-25', 'placeholder': '123', 'id': 'cvv', 'maxlength': '3'}))

    amount = forms.CharField(label='amount', widget=forms.TextInput(attrs={'class': 'form-control form-shadow-sm w-25', 'placeholder': '123.4'}))