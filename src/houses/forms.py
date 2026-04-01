from django import forms
from extra_views import InlineFormSetFactory

from src.houses.models import House, Storey, Section


class HouseForm(forms.ModelForm):
    class Meta:
        model = House

        fields = ['name', 'adress', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5']


        widgets = {
            'name': forms.TextInput(attrs={'id': "houseform-name", 'name': 'HouseForm[name]', 'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'id': "houseform-adress", 'name': 'HouseForm[adress]', 'class': 'form-control'}),
            'image_1': forms.FileInput(attrs={'type': 'file', 'id': 'houseform-image1', 'name': 'HouseForm[image1]'}),
            'image_2': forms.FileInput(attrs={'type': 'file', 'id': 'houseform-image2', 'name': 'HouseForm[image2]'}),
            'image_3': forms.FileInput(attrs={'type': 'file', 'id': 'houseform-image3', 'name': 'HouseForm[image3]'}),
            'image_4': forms.FileInput(attrs={'type': 'file', 'id': 'houseform-image4', 'name': 'HouseForm[image4]'}),
            'image_5': forms.FileInput(attrs={'type': 'file', 'id': 'houseform-image5', 'name': 'HouseForm[image5]'}),
        }


class SectionFormSet(InlineFormSetFactory):
    model = Section
    fields = ['name']
    factory_kwargs = {'extra': 1, 'can_delete': True}







#< input
# type = "file"
# id = "houseform-image4"
# name = "HouseForm[image4]"
# accept = "image/*" >


# <input type="text" id="houseform-name" class="form-control" name="HouseForm[name]">

#'name_uk': forms.TextInput(attrs={'class': 'col-sm-6"'}),
