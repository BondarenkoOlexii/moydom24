from django import forms
from django.forms import inlineformset_factory

from src.houses.models import House, Storey, Section, Worker, Apartment, Call_Master
from src.users.models import User, Role


class HouseForm(forms.ModelForm):
    image_1 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'houseform-image1'}),
        label="Фотографія 1"
    )
    image_2 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'houseform-image2'}),
        label="Фотографія 2"
    )
    image_3 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'houseform-image3'}),
        label="Фотографія 3"
    )
    image_4 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'houseform-image4'}),
        label="Фотографія 4"
    )
    image_5 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'houseform-image5'}),
        label="Фотографія 5"
    )


    class Meta:
        model = House

        fields = ['name', 'adress']

        widgets = {
            'name': forms.TextInput(attrs={'id': "houseform-name", 'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'id': "houseform-adress", 'class': 'form-control'}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section

        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'id': "houseform-name", 'name': 'HouseForm[name]', 'class': 'form-control'}),
        }


SectionInlineFormSet = inlineformset_factory(
    House,
    Section,
    form=SectionForm,
    extra=0,
    can_delete=False
)


class StoreyForm(forms.ModelForm):
    class Meta:
        model = Storey

        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'id': "houseform-name", 'name': 'HouseForm[name]', 'class': 'form-control'}),
        }


StoreyInlineFormSet = inlineformset_factory(
    House,
    Storey,
    form=StoreyForm,
    extra=0,
    can_delete=False
)


class HousesAdmin(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Worker.objects.all(), empty_label='',
                                  widget=forms.Select(attrs={'id': "houseform-name", 'name': 'HouseForm[name]', 'class': 'form-control useradmin-select'}))

    class Meta:
        model = Worker

        fields = ['role']

        widgets = {
            'role': forms.TextInput(attrs={'id': "houseform-name", 'name': 'HouseForm[name]', 'class': 'form-control'})
        }

HousesAdminInlineFormSet = inlineformset_factory(
    House,
    Worker,
    form=HousesAdmin,
    extra=0,
    can_delete=False
)


class ApartmentForm(forms.ModelForm):
   owner = forms.ModelChoiceField(queryset=User.objects.all(), label="", widget=forms.Select(
        attrs={'class': 'form-control', 'id': 'select2-flatform-user_id-container'}))



   class Meta:
        model = Apartment
        fields = ['area', 'apartment_number', 'owner', 'house', 'section', 'storey']

        widgets = {
            'area': forms.TextInput(attrs={'id': 'flatform-square', 'class': 'form-control'}),
            'apartment_number': forms.TextInput(attrs={'id': 'flatform-flat', 'class': 'form-control', 'aria-required': 'true'}),
            'house': forms.Select(attrs={'id': 'flatform-house_id', 'class': 'form-control'}),
            'section': forms.Select(attrs={'id': 'flatform-section_id', 'class': 'form-control'}),
            'storey': forms.Select(attrs={'id': 'flatform-floor_id', 'class': 'form-control'}),
        }




class MasterRequestForm(forms.ModelForm):

    class Meta:
        model = Call_Master
        fields = ['user', 'data_create', 'сonvenient_time', 'description', 'comment', 'status', 'role', 'apartment', 'master']

        widgets = {
            'user': forms.Select(attrs={'id': 'user-container', 'class': 'form-control'}),
            'master': forms.Select(attrs={'id': 'masterrequest-user_admin_id', 'class': 'form-control'}),
            'apartment': forms.Select(attrs={'id': 'select2-masterrequest-flat_id-container', 'class': 'form-control'}),
            'data_create': forms.DateInput(attrs={'id': 'masterrequest-date_request', 'class': 'form-control krajee-datepicker', 'name': 'MasterRequest[date_request]',
                                                  'data-datepicker-source':'masterrequest-date_request-kvdate', 'data-datepicker-type': '3', 'data-krajee-kvdatepicker': 'kvDatepicker_1643d6f1'}),

            'сonvenient_time': forms.TimeInput(attrs={'id': 'masterrequest-time_request', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'masterrequest-description', 'class': 'compose-textarea form-control', 'rows': '6', 'placeholder': 'Текст сообщения'}),
            'comment': forms.Textarea(attrs={'id': 'message-description', 'class': 'compose-textarea form-control'}),
            'status': forms.Select(attrs={'id': 'masterrequest-status', 'class': 'form-control'}),
            'role': forms.Select(attrs={'id': 'masterrequest-type', 'class': 'form-control', 'value': ''}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['role'].initial = 'director'

# class SectionFormSet(InlineFormSetFactory):
#     model = Section
#     fields = ['name']
#     factory_kwargs = {'extra': 1, 'can_delete': True}


# < input
# type = "file"
# id = "houseform-image4"
# name = "HouseForm[image4]"
# accept = "image/*" >


# <input type="text" id="houseform-name" class="form-control" name="HouseForm[name]">

# 'name_uk': forms.TextInput(attrs={'class': 'col-sm-6"'}),
