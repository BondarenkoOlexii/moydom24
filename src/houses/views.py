from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from src.adminpanel.mixin import AdminpanelRestrictionMixin
from .models import House, Section, Image, Apartment, Call_Master
from .forms import HouseForm, SectionInlineFormSet, StoreyInlineFormSet, HousesAdminInlineFormSet, ApartmentForm,\
    MasterRequestForm


# Create your views here.


class ListHouse(AdminpanelRestrictionMixin, ListView):
    required_section = 'house'

    model = House
    template_name = 'house.html'
    context_object_name = 'houses'  #кастомна назва до якої ми звертаємось в шаблоні

class DetailHouse(AdminpanelRestrictionMixin, DetailView):
    required_section = 'house'

    model = House
    template_name = 'show_house.html'
    context_object_name = 'house'

class CreateHouse(AdminpanelRestrictionMixin, CreateView):
    required_section = 'house'

    template_name = 'create_user.html'
    model = House
    form_class = HouseForm

    def get_context_data(self, **kwargs):
        ctx = super(CreateHouse, self).get_context_data(**kwargs)
        if 'inlines' not in ctx:
            ctx['inlines'] = SectionInlineFormSet(prefix='sections')
        if 'inlines_2' not in ctx:
            ctx['inlines_2'] = StoreyInlineFormSet(prefix='storey')
        if 'inlines_3' not in ctx:
            ctx['inlines_3'] = HousesAdminInlineFormSet(prefix='worker')
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None

        form = self.get_form()
        inlines = SectionInlineFormSet(request.POST, prefix='sections')
        inlines_2 = StoreyInlineFormSet(request.POST, prefix='storey')
        inlines_3 = HousesAdminInlineFormSet(request.POST, prefix='worker')

        if form.is_valid() and inlines.is_valid() and inlines_2.is_valid() and inlines_3.is_valid(): # imageform.is_valid()
            return self.form_valid(form, inlines, inlines_2, inlines_3)
        else:
            return self.form_invalid(form, inlines, inlines_2, inlines_3)


    def form_valid(self, form, inlines, inlines_2, inlines_3):
        print("а це працює")

        self.object = form.save(commit=False)

        img_list = ['image_1', 'image_2', 'image_3', 'image_4', 'image_5']

        for img in img_list:
            field_name = img
            img_obj = form.cleaned_data.get(img)
            if img_obj:
                upload_img = Image.objects.create(photo=img_obj)

                setattr(self.object, field_name, upload_img)


        self.object.save()

        inlines.instance = self.object
        inlines.save()

        inlines_2.instance = self.object
        inlines_2.save()

        inlines_3.instance = self.object
        inlines_3.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, inlines, inlines_2, inlines_3):
        print(form.errors)
        print(inlines.errors)
        print(inlines_2.errors)
        print(inlines_3.errors)
        return self.render_to_response(self.get_context_data(form=form, inlines=inlines,
                                                             inlines_2=inlines_2, inlines_3=inlines_3))

    def get_success_url(self):
        return reverse('house')



class UpdateHouse(AdminpanelRestrictionMixin, UpdateView):
    required_section = 'house'

    template_name = 'create_user.html'
    model = House
    form_class = HouseForm


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self.object = self.get_object()

        if 'inlines' not in ctx:
            ctx['inlines'] = SectionInlineFormSet(instance=self.object, prefix='sections')
        if 'inlines_2' not in ctx:
            ctx['inlines_2'] = StoreyInlineFormSet(instance=self.object, prefix='storey')
        if 'inlines_3' not in ctx:
            ctx['inlines_3'] = HousesAdminInlineFormSet(instance=self.object, prefix='worker')
        return ctx


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        inlines = SectionInlineFormSet(request.POST, instance=self.object, prefix='sections')
        inlines_2 = StoreyInlineFormSet(request.POST, instance=self.object, prefix='storey')
        inlines_3 = HousesAdminInlineFormSet(request.POST, instance=self.object,  prefix='worker')

        if form.is_valid() and inlines.is_valid() and inlines_2.is_valid() and inlines_3.is_valid(): # imageform.is_valid()
            return self.form_valid(form, inlines, inlines_2, inlines_3)
        else:
            return self.form_invalid(form, inlines, inlines_2, inlines_3)

    def form_valid(self, form, inlines, inlines_2, inlines_3):
        print("а це працює")

        self.object = form.save(commit=False)

        img_list = ['image_1', 'image_2', 'image_3', 'image_4', 'image_5']

        for img in img_list:
            if img in form.changed_data:
                field_name = img
                img_obj = form.cleaned_data.get(img)
                if img_obj:
                    upload_img = Image.objects.create(photo=img_obj)

                    setattr(self.object, field_name, upload_img)


        self.object.save()

        inlines.instance = self.object
        inlines.save()

        inlines_2.instance = self.object
        inlines_2.save()

        inlines_3.instance = self.object
        inlines_3.save()

        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form, inlines, inlines_2, inlines_3):
        print(form.errors)
        print(inlines.errors)
        print(inlines_2.errors)
        print(inlines_3.errors)
        return self.render_to_response(self.get_context_data(form=form, inlines=inlines,
                                                             inlines_2=inlines_2, inlines_3=inlines_3))

    def get_success_url(self):
        return reverse('house')

class DeleteHouse(AdminpanelRestrictionMixin, DeleteView):
    required_section = 'house'

    model = House
    success_url = reverse_lazy('house')


class ApartmentList(AdminpanelRestrictionMixin, ListView):
    required_section = 'apartments'

    model = Apartment
    template_name = 'apartment.html'
    context_object_name = 'apartments'

class DetailApartment(AdminpanelRestrictionMixin, DetailView):
    required_section = 'apartments'

    model = Apartment
    template_name = 'show_apart.html'
    context_object_name = 'apartment'

class CreateApartment(AdminpanelRestrictionMixin, CreateView):
    required_section = 'apartments'

    model = Apartment
    template_name = 'create_apartment.html'
    form_class = ApartmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['all_data'] = House.objects.all()
        return context

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('apartment')


class UpdateApartment(AdminpanelRestrictionMixin, UpdateView):
    required_section = 'apartments'

    model = Apartment
    template_name = 'create_apartment.html'
    form_class = ApartmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        context['all_data'] = House.objects.all()
        return context

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('apartment')


class DeleteApartmnent(AdminpanelRestrictionMixin, DeleteView):
    required_section = 'apartments'

    model = Apartment
    success_url = reverse_lazy('apartment')



class ListMasterRequest(AdminpanelRestrictionMixin, ListView):
    required_section = 'call_master'

    model = Call_Master
    template_name = 'master-request.html'
    context_object_name = 'masters'


class NewMasterRequest(AdminpanelRestrictionMixin, CreateView):
    required_section = 'call_master'

    model = Call_Master
    template_name = 'new-master-request.html'
    form_class = MasterRequestForm
    success_url = reverse_lazy('request-master-list')


class UpdateMasterRequest(AdminpanelRestrictionMixin, UpdateView):
    required_section = 'call_master'

    model = Call_Master
    template_name = 'new-master-request.html'
    form_class = MasterRequestForm
    success_url = reverse_lazy('request-master-list')


class DeleteMasterRequest(AdminpanelRestrictionMixin, DeleteView):
    required_section = 'call_master'

    model = Call_Master
    success_url = reverse_lazy('request-master-list')