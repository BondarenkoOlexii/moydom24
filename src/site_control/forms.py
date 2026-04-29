from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Main_Page, About_Page, SeoBlock, Additional_Block, Additional_File, Contact_Page

# Seo Block


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ['title', 'keyword', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'id': 'websitehomeform-homemetatitle', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'websitehomeform-homemetadescription', 'class': 'form-control'}),
            'keyword': forms.Textarea(attrs={'id': 'websitehomeform-homemetakeywords', 'class': 'form-control'})
        }


# Main Page


class MainPageForm(forms.ModelForm):
    image_1 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'websitehomeslide-0-id'}),
        label="Фотографія 1"
    )
    image_2 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'websitehomeslide-1-id'}),
        label="Фотографія 2"
    )
    image_3 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'websitehomeslide-2-id'}),
        label="Фотографія 3"
    )

    class Meta:
        model = Main_Page
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'id': 'websitehomeform-hometitle', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'message-description', 'class': 'compose-textarea form-control'}),
        }


# About Page


class AboutPageForm(forms.ModelForm):

    manager_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'websiteaboutform-imagefile', 'name': 'WebsiteAboutForm[imageFile]'}),
        label="Фотографія менеджера"
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'websitehomeslide-id'}),
        label="Фотографія"
    )

    class Meta:
        model = About_Page
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'id':'websiteaboutform-abouttitle2', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'message-description', 'class': 'compose-textarea form-control'}),
        }


# Form for Contact Page


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact_Page
        fields = ['name', 'description', 'url', 'coordinate',
                  'full_name', 'location', 'adress', 'email_adress', 'phone_number']

        widgets = {
            'name': forms.TextInput(attrs={'id': 'websitecontactform-contacttitle', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'id': 'message-description', 'class': 'compose-textarea form-control'}),
            'url': forms.URLInput(attrs={'id': 'websitecontactform-contacturlsite', 'class': 'form-control'}),
            'coordinate': forms.Textarea(attrs={'id': 'websitecontactform-contactmapembedcode', 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'id': 'websitecontactform-contactfullname', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'id': 'websitecontactform-contactlocation', 'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'id': 'websitecontactform-contactaddress', 'class': 'form-control'}),
            'email_adress': forms.EmailInput(attrs={'id': 'websitecontactform-contactemail', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'id': 'websitecontactform-contactphone', 'class': 'form-control'})
        }



# Additional Form for Main Page


class AdditionalForm(forms.ModelForm):
    additional_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'id': 'websitehomefeature-imagefile'}),
        label="Фотографія 1"
    )

    class Meta:
        model = Additional_Block
        fields = ['additional_name', 'additional_description']

        widgets = {
            'additional_name': forms.TextInput(attrs={'id': 'websitehomefeature-id', 'class': 'form-control'}),
            'additional_description': forms.Textarea(attrs={'id': 'message-description', 'class': 'compose-textarea form-control'}),
        }

AdditionalMainFormSet = inlineformset_factory(Main_Page, Additional_Block, AdditionalForm, extra=6, can_delete=False)


# Additional Form for About Page

class AdditionalFileForm(forms.ModelForm):
    class Meta:
        model = Additional_File
        fields = ['additional_file', 'file_name']

AdditionalAboutFileFormSet = inlineformset_factory(About_Page, Additional_File, AdditionalFileForm, extra=1, can_delete=True)


# Form for Service Page

ServiceFormSet = modelformset_factory(Additional_Block, AdditionalForm, extra=1, can_delete=True)
