from django import forms
from .models import User


class UserForm(forms.ModelForm):

    main_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'userform-image', 'name': 'UserForm[image]'}),
        label="Фотографія"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pass-value', 'id': 'userform-password'}),
        label="Пароль",
        required=False  # Якщо це UpdateView, пароль не обов'язковий
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pass-value', 'id': 'userform-password2'}),
        label="Повторіть пароль",
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'language', 'phone_number', 'telegram', 'date_of_birth', 'notes', 'user_status', 'email', 'viber', 'password', 'password_confirm', 'user_id']

        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'userform-firstname', 'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'id': 'userform-middlename', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'id': 'userform-lastname', 'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'id': 'userform-birthdate', 'class': 'form-control krajee-datepicker',
                                                    'name': 'UserForm[birthdate]', 'data-datepicker-source': 'userform-birthdate-kvdate', 'data-datepicker-type': '3', 'data-krajee-kvdatepicker': 'kvDatepicker_1643d6f1'}),

            'notes': forms.Textarea(attrs={'id': 'userform-note', 'class': 'form-control', 'rows': '10', 'style': 'height: 256px'}),

            'phone_number':  forms.TextInput(attrs={'id': 'userform-phone', 'class': 'form-control'}),
            'viber': forms.TextInput(attrs={'id': 'userform-viber', 'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'id': 'userform-telegram', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'id': 'userform-email', 'class': 'form-control', 'aria-required': 'true'}),
            'user_status': forms.Select(attrs={'id': 'userform-status', 'class': 'form-control', 'aria-invalid': 'false'}),
            'user_id': forms.TextInput(attrs={'id': 'userform-uid', 'class': 'form-control'})
        }

# password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'}))
# password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control pass-value'}))

# class CustomChangePassword(SetPasswordForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.fields['password1'].required = False
#         self.fields['password2'].required = False
#
#
#         place_holders = {
#             'password1': 'Пароль',
#             'password2': 'Повторить пароль'
#         }
#
#         for field_name, text in place_holders.items():
#             if field_name in self.fields:
#                 self.fields[field_name].widget.attrs.update({
#                     'class': 'form-control',
#                     'placeholder': text
#                 })
