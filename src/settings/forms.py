from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import PaymentInfo, TransactionPurpose, Service, Measurement, Tariff, Tarrif_Service_Price, Counters
from src.users.models import Role


class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ['name', 'information']

        widgets = {
            'name': forms.TextInput(attrs={'id': '', 'class': 'form-control'}),
            'information': forms.Textarea(attrs={'id': 'paycompany-0-description', 'class': 'form-control'})
        }


class TransactionPurposeForm(forms.ModelForm):
    class Meta:
        model = TransactionPurpose
        fields = ['name', 'type']

        widgets = {
            'name': forms.TextInput(attrs={'id': 'transactionpurpose-name', 'class': 'form-control'}),
            'type': forms.Select(attrs={'id': 'transactionpurpose-type', 'class': 'form-control'})
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service', 'show', 'measurement']

        widgets = {
            'service': forms.TextInput(attrs={'id': 'service-name', 'class': 'form-control'}),
            'show': forms.CheckboxInput(attrs={'id': 'service-is_counter', 'type': 'checkbox'}),
            'measurement': forms.Select(attrs={'class': 'form-control'})
        }


ServiceFormSet = modelformset_factory(Service, ServiceForm, extra=1, can_delete=True)


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['unit_of_measurement']

        widgets = {
            'unit_of_measurement': forms.TextInput(attrs={'id': 'serviceunit-name', 'class': 'form-control'})
        }


MeasurementFormSet = modelformset_factory(Measurement, MeasurementForm, extra=1, can_delete=True)






class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'id': 'tariff-name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'tariff-description', 'class': 'form-control'})
        }


# class ServiceSelectWidget(forms.Select):
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#
#         option = super().create_option(name, value, label, selected, index, subindex, attrs)
#
#         if value:
#
#             value_id = getattr(value, 'value', value)
#
#             service_obj = self.choices.queryset.get(pk=value_id)
#
#
#             if service_obj.measurement:
#                 option['attrs']['data-measurement'] = service_obj.measurement.unit_of_measurement
#             else:
#                 option['attrs']['data-measurement'] = ''
#         return option


class ThourghTarrifServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control service-select'})
    )

    class Meta:
        model = Tarrif_Service_Price
        fields = ['price', 'service']

        widgets = {
            'price': forms.TextInput(attrs={'id': 'tariffservice-price_unit', 'class': 'form-control'}),
        }


TariffFormSet = inlineformset_factory(Tariff, Tarrif_Service_Price, form=ThourghTarrifServiceForm, extra=1, can_delete=True)


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['statistics', 'transaction', 'receipts', 'payment_account', 'apartments', 'apartments_owner', 'house', 'messages',
                  'call_master', 'counters', 'site_control', 'services', 'tariff', 'role_list', 'users', 'payment_data']


        widgets = {
            field: forms.CheckboxInput(attrs={'class': 'text-center'})
            for field in fields
        }



class CounterForm(forms.ModelForm):
    class Meta:
        model = Counters
        fields = ['special_id', 'indicator', 'status', 'create_time', 'service', 'apartment']

        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'apartment': forms.Select(attrs={'id': 'flatform-flat_id', 'class': 'form-control'}),
            'special_id': forms.TextInput(attrs={'id': 'counterdata-uid', 'class': 'form-control'}),
            'indicator': forms.NumberInput(attrs={'id': 'counterdata-amount_total', 'class': 'form-control', 'step': '0.1', 'min': '0'}),
            'status': forms.Select(attrs={'id': 'counterdata-status', 'class': 'form-control'}),
            'create_time': forms.DateInput(attrs={'id': 'counterdata-uid_date', 'class': 'form-control krajee-datepicker', 'name': 'MasterRequest[date_request]',
                                                  'data-datepicker-source':'masterrequest-date_request-kvdate', 'data-datepicker-type': '3', 'data-krajee-kvdatepicker': 'kvDatepicker_1643d6f1'})
        }