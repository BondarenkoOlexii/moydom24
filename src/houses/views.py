from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import House, Section, Image, Apartment
from .forms import HouseForm, SectionInlineFormSet, StoreyInlineFormSet, HousesAdminInlineFormSet, ApartmentForm
# Create your views here.


class ListHouse(ListView):
    model = House
    template_name = 'house.html'
    context_object_name = 'houses'  #кастомна назва до якої ми звертаємось в шаблоні
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        search_name_query = self.request.GET.get('HouseSearch[name]', '')
        search_adress_query = self.request.GET.get('HouseSearch[address]', '')

        if search_name_query:
            queryset = queryset.filter(name__icontains=search_name_query)

        if search_adress_query:
            queryset = queryset.filter(adress__icontains=search_adress_query)

        return queryset

class CreateHouse(CreateView):
    template_name = 'create_house.html'
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



class UpdateHouse(UpdateView):
    template_name = 'create_house.html'
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
            if not img.has_changed():
                continue
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

class DeleteHouse(DeleteView):
    model = House
    success_url = reverse_lazy('house')



class ApartmentList(ListView):
    model = Apartment
    template_name = 'apartment.html'
    context_object_name = 'apartments'


class CreateApartment(CreateView):
    model = Apartment
    template_name = 'create_apartment.html'
    form_class = ApartmentForm

