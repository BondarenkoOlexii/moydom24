from django import forms
from .models import User, Message, Role
from src.houses.models import House, Section, Storey, Apartment
from src.adminpanel.models import UserChoise
from django_select2.forms import ModelSelect2Widget

class UserForm(forms.ModelForm):

    main_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'userform-image', 'name': 'UserForm[image]'}),
        label="Фотографія"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pass-value', 'id': 'userform-password'}),
        label="Пароль",
        required=False
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

        def __init__(self, *args, **kwargs):
            user = kwargs.pop("user", None)

            super().__init__(*args, **kwargs)

            if user and not user.is_superuser and not user.is_staff:
                self.fields['user_id'].widget.attrs["readonly"] = True



class MessageForm(forms.Form):
    theme = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'message-name', 'class': 'form-control'})
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'message-description',
            'class': 'compose-textarea form-control',
            'rows': '6',
            'placeholder': 'Текст сообщения'
        })
    )
    # user = forms.ModelChoiceField(
    #     queryset=User.objects.all(),
    #     widget=forms.Select(attrs={'id': 'messageaddress-flat_id', 'class': 'form-control'})
    # )
    house = forms.ModelChoiceField(
        queryset=House.objects.all(),
        widget=forms.Select(attrs={'id': 'flatform-house_id', 'class': 'form-control'}),
        required=False
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        widget=forms.Select(attrs={'id': 'flatform-section_id', 'class': 'form-control'}),
        required=False
    )
    storey = forms.ModelChoiceField(
        queryset=Storey.objects.all(),
        widget=forms.Select(attrs={'id': 'flatform-floor_id', 'class': 'form-control'}),
        required=False
    )
    apartment = forms.ModelChoiceField(
        queryset=Apartment.objects.all(),
        widget=forms.Select(attrs={'id': 'flatform-flat_id', 'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop('instance', None)

        super(MessageForm, self).__init__(*args, **kwargs)

        # Для того, аби select2 коректно працював з ModelChoiseField, ми очищуємо поля аби select2 підставив свої дані,
        # тобто ми підтягуємо спочатку дані щоб джанга не ругалась а після чистимо їх і даємо знову заповнити
        if not self.is_bound:
            self.fields['section'].queryset = Section.objects.none()
            self.fields['storey'].queryset = Storey.objects.none()
            self.fields['apartment'].queryset = Apartment.objects.none()



class InviteMessage(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'info@example.com'})
    )

class CreateMasterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pass-value', 'id': 'userform-password'}),
        label="Пароль",
        required=False
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control pass-value', 'id': 'userform-password2'}),
        label="Повторіть пароль",
        required=False
    )

    role_select = forms.ChoiceField(
        choices=UserChoise.Roles.choices,
        label='Виберіть роль',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'password_confirm', 'user_status', 'role_select']

        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'userform-firstname', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'id': 'userform-lastname', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'id': 'userform-phone', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'id': 'userform-email', 'class': 'form-control', 'aria-required': 'true'}),
            'user_status': forms.Select(attrs={'id': 'useradminform-status', 'class': 'form-control'})
        }


# 'id': 'userform-birthdate', 'class': 'form-control krajee-datepicker', 'name': 'UserForm[birthdate]', 'data-datepicker-source': 'userform-birthdate-kvdate', 'data-datepicker-type': '3', 'data-krajee-kvdatepicker': 'kvDatepicker_1643d6f1'
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['role_select'].label_from_instance = lambda obj: f"{obj.role}"







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
