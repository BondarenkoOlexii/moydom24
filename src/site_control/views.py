from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View

from .models import Main_Page, About_Page, Contact_Page, Additional_Block
from .forms import SeoBlockForm, MainPageForm, AdditionalMainFormSet, AboutPageForm, AdditionalForm,\
    AdditionalAboutFileFormSet, ContactForm, ServiceFormSet
from src.adminpanel.models.SiteChoise import PageChoise
from src.common.models import Image


# Create your views here.


class CreateMainPageView(UpdateView):
    model = Main_Page
    template_name = 'back_main.html'
    form_class = MainPageForm
    success_url = reverse_lazy('website-main')

    def get_object(self, queryset=None):
        try:
            main_obj = Main_Page.objects.first()
            return main_obj
        except(AttributeError, Main_Page.DoesNotExist):
            return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        seo_instance = getattr(self.object, 'seoblock', None) if self.object else None

        if self.request.POST:
            ctx['seoform'] = SeoBlockForm(self.request.POST, self.request.FILES, prefix='seoblock', instance=seo_instance)
            ctx['formset'] = AdditionalMainFormSet(self.request.POST, self.request.FILES, prefix='formset', instance=self.object)
        else:
            ctx['seoform'] = SeoBlockForm(prefix='seoblock', instance=seo_instance)
            ctx['formset'] = AdditionalMainFormSet(prefix='formset', instance=self.object)
        return ctx
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        seoform = SeoBlockForm(request.POST, request.FILES, prefix='seoblock')
        formset = AdditionalMainFormSet(request.POST, request.FILES, prefix='formset')


        if form.is_valid() and seoform.is_valid() and formset.is_valid():
            return self.form_valid(form, seoform, formset)
        else:
            return self.form_invalid(form, seoform, formset)


    def form_valid(self, form, seoform, formset):
        seo_instance = seoform.save()

        self.object = form.save(commit=False)

        self.object.seoblock = seo_instance
        form.cleaned_data['type'] = PageChoise.main

        img_list = ['image_1', 'image_2', 'image_3']

        for img in img_list:
            field_name = img
            img_obj = form.cleaned_data.get(img)
            print(img_obj)
            if img_obj:
                upload_img = Image.objects.create(photo=img_obj)
                print(upload_img)
                setattr(self.object, field_name, upload_img)

        form.save()

        formset.instance = self.object
        formset.save()

        return self.get_success_url()


    def form_invalid(self, form, seoform, formset):
        print(form.errors)
        print(seoform.errors)
        print(formset.errors)
        return self.render_to_response(self.get_context_data(form=form, seoform=seoform, formset=formset))

    def get_success_url(self):
        return redirect('website-main')







class CreateAboutPageView(UpdateView):
    model = About_Page
    template_name = 'back_about.html'
    form_class = AboutPageForm
    success_url = reverse_lazy('website-about')

    def get_object(self, queryset=None):
        try:
            about_obj = About_Page.objects.first()
            return about_obj
        except(AttributeError, About_Page.DoesNotExist):
            return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        seo_instance = getattr(self.object, 'seoblock', None) if self.object else None

        additional_instance = getattr(self.object, 'additional_block', None) if self.object else None

        if 'seoform' not in ctx:
            ctx['seoform'] = SeoBlockForm(prefix='seoblock', instance=seo_instance)

        if 'additional_form' not in ctx:
            ctx['additional_form'] = AdditionalForm(prefix='additional_form', instance=additional_instance)

        if 'formset' not in ctx:
            ctx['formset'] = AdditionalAboutFileFormSet(prefix='file_formset', instance=self.object)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        seo_instance = getattr(self.object, 'seoblock', None) if self.object else None
        additional_instance = getattr(self.object, 'additional_block', None) if self.object else None

        form = self.get_form()

        seoform = SeoBlockForm(request.POST, request.FILES, prefix='seoblock', instance=seo_instance)
        additional_form = AdditionalForm(request.POST, request.FILES, prefix='additional_form', instance=additional_instance)
        formset = AdditionalMainFormSet(request.POST, request.FILES, prefix='file_formset', instance=self.object)


        if form.is_valid() and seoform.is_valid() and formset.is_valid() and additional_form.is_valid():
            return self.form_valid(form, seoform, formset, additional_form)
        else:
            return self.form_invalid(form, seoform, formset, additional_form)

    def form_valid(self, form, seoform, formset, additional_form):
        seo_instance = seoform.save()

        self.object = form.save(commit=False)

        self.object.seoblock = seo_instance

        images = self.request.FILES.getlist('gallery_images')

        for image in images:
            upload_img = Image.objects.create(photo=image)
            self.object.image.add(upload_img)

        # img_list = ['image_1', 'image_2', 'image_3']
        #
        # for img in img_list:
        #     field_name = img
        #     img_obj = form.cleaned_data.get(img)
        #     print(img_obj)
        #     if img_obj:
        #         upload_img = Image.objects.create(photo=img_obj)
        #         print(upload_img)
        #         setattr(self.object, field_name, upload_img)

        form.save()

        formset.instance = self.object
        formset.save()

        additional_form.instance = self.object
        additional_form.save()

        return self.get_success_url()

    def form_invalid(self, form, seoform, formset, additional_form):
        print(form.errors)
        print(seoform.errors)
        print(formset.errors)
        print(additional_form.errors)
        return self.render_to_response(self.get_context_data(form=form, seoform=seoform, formset=formset, additional_form=additional_form))


    
class CreateContactPageView(UpdateView):
    model = Contact_Page
    template_name = 'back_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('website-contact')

    def get_object(self, queryset=None):
        try:
            contact_obj = Contact_Page.objects.first()
            return contact_obj
        except(AttributeError, Contact_Page.DoesNotExist):
            return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        seo_instance = getattr(self.object, 'seoblock', None) if self.object else None

        if self.request.POST:
            ctx['seoform'] = SeoBlockForm(self.request.POST, self.request.FILES, prefix='seoblock', instance=seo_instance)
        else:
            ctx['seoform'] = SeoBlockForm(prefix='seoblock', instance=seo_instance)
        return ctx
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        seoform = SeoBlockForm(request.POST, request.FILES, prefix='seoblock')

        if form.is_valid() and seoform.is_valid():
            return self.form_valid(form, seoform)
        else:
            return self.form_invalid(form, seoform)


    def form_valid(self, form, seoform):
        seo_instance = seoform.save()

        self.object = form.save(commit=False)

        self.object.seoblock = seo_instance

        form.save()

        return self.get_success_url()


    def form_invalid(self, form, seoform):
        print(form.errors)
        print(seoform.errors)
        return self.render_to_response(self.get_context_data(form=form, seoform=seoform))

    def get_success_url(self):
        return redirect('website-contact')




class CreateServicePageView(View):
    template_name = 'back_service.html'
    success_url = 'website-service'

    def get_queryset(self):

        return Additional_Block.objects.filter(main_page__isnull=True, about_page__isnull=True)

    def get(self, request, *args, **kwargs):
        formset = ServiceFormSet(queryset=self.get_queryset())
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = ServiceFormSet(data=request.POST, files=request.FILES, queryset=self.get_queryset())

        if formset.is_valid():
            formset.save(commit=False)

            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    continue

                if form.has_changed():
                    img_file = form.cleaned_data.get('additional_image')

                    if img_file:
                        new_image = Image.objects.create(photo=img_file)
                        form.instance.additional_image = new_image

                    form.instance.save()

                for obj in formset.deleted_objects:
                    obj.delete()

                return redirect(self.success_url)
        return render(request, self.template_name, {'formset': formset})