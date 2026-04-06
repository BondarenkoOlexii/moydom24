from django import forms
from django.forms import inlineformset_factory

from src.houses.models import House, Storey, Section, Worker


class HouseForm(forms.ModelForm):
    class Meta:
        model = House

        fields = ['name', 'adress']

        widgets = {
            'name': forms.TextInput(attrs={'id': "houseform-name", 'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'id': "houseform-adress", 'class': 'form-control'}),
        }


class ImageForm(forms.Form):
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
