from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from datetime import datetime

from src.adminpanel.mixin import AdminpanelRestrictionMixin
from .models import PaymentInfo, TransactionPurpose, Service, Measurement, Tariff, Tarrif_Service_Price, Counters
from src.users.models import Role
from src.houses.models import House

from .forms import PaymentInfoForm, TransactionPurposeForm, ServiceFormSet, ServiceForm, MeasurementFormSet,\
    MeasurementForm, TariffForm, TariffFormSet, RoleForm, CounterForm

# Create your views here.





class RoleView(AdminpanelRestrictionMixin, ListView):
    required_section = 'role_list'

    model = Role
    template_name = 'role.html'
    # form_class = RoleForm
    context_object_name = 'roles'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if 'form' not in ctx:
            ctx['form'] = RoleForm()

            ctx['roles_for_forms'] = [
                RoleForm(instance=role, prefix=f'role_{role.id}') for role in ctx['roles']
            ]

        return ctx

    def post(self, request, *args, **kwargs):
        all_role = Role.objects.all()

        for role in all_role:
            form = RoleForm(request.POST, instance=role, prefix=f'role_{role.id}')

            if form.is_valid():
                role_display = role.get_role_display()
                changes = form.cleaned_data

                print(f"Зміни для: {role_display} (ID: {role.id})")
                print(f"Змінені поля: {changes}")

                form.save()

        print(request.POST)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('role')

class PaymentInfoCreate(AdminpanelRestrictionMixin, CreateView):
    required_section = 'payment_data'

    model = PaymentInfo
    template_name = 'pay-company.html'
    form_class = PaymentInfoForm
    success_url = 'pay-company'

    def get_object(self, queryset=None):
        try:
            paymentinfo = PaymentInfo.objects.first()
            return paymentinfo
        except(AttributeError, PaymentInfo.DoesNotExist):
            return None


class TransactionProposeList(AdminpanelRestrictionMixin, ListView):
    required_section = 'transaction_propose'

    model = TransactionPurpose
    template_name = 'transaction-purpose.html'
    context_object_name = 'form'

class TransactionProposeCreate(AdminpanelRestrictionMixin, CreateView):
    required_section = 'transaction_propose'

    model = TransactionPurpose
    template_name = 'transaction-purpose_create.html'
    form_class = TransactionPurposeForm
    success_url = reverse_lazy('transaction-purpose')

class TransactionProposeUpdate(AdminpanelRestrictionMixin, UpdateView):
    required_section = 'transaction_propose'

    model = TransactionPurpose
    template_name = 'transaction-purpose_create.html'
    form_class = TransactionPurposeForm
    success_url = 'transaction-purpose'

class TransactionProposeDelete(AdminpanelRestrictionMixin, DeleteView):
    required_section = 'transaction_propose'

    model = TransactionPurpose
    success_url = reverse_lazy('transaction-purpose')




class ServiceView(AdminpanelRestrictionMixin, TemplateView):
    required_section = 'services'

    template_name = 'service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'formset' not in context:
            context['formset'] = ServiceFormSet(queryset=Service.objects.all(), prefix='service')
        if 'formset_measurement' not in context:
            context['formset_measurement'] = MeasurementFormSet(queryset=Measurement.objects.all(), prefix='measurement')

        return context
    def post(self, request, *args, **kwargs):
        formset = ServiceFormSet(request.POST, queryset=Service.objects.all(), prefix='service')
        formset_measurement = MeasurementFormSet(request.POST, queryset=Measurement.objects.all(), prefix='measurement')

        if formset.is_valid() and formset_measurement.is_valid():
            obj_formset = formset.save()
            formset_measurement.service = obj_formset
            formset_measurement.save()
            return redirect(self.get_success_url())
        else:
            print(f"Проблема в формсеті звичайному {formset.errors}")
            print(f"Проблема в формсеті незвичайному {formset_measurement.errors}")


        return super().render_to_response(self.get_context_data(
            formset=formset,
            formset_measurement=formset_measurement
        ))

    def get_success_url(self):
        return reverse('service')


class TariffList(AdminpanelRestrictionMixin, ListView):
    required_section = 'tariff'

    model = Tariff
    template_name = 'tariff.html'
    context_object_name = 'form'


class CreateTariff(AdminpanelRestrictionMixin, CreateView):
    required_section = 'tariff'


    model = Tariff
    template_name = 'create_tariff.html'
    form_class = TariffForm

    def get_initial(self):
        initial = super().get_initial()

        tariff_id = self.request.GET.get('tariff_id')

        if tariff_id:
            source_tariff = Tariff.objects.filter(id=tariff_id).first()
            if source_tariff:
                initial['name'] = source_tariff.name
                initial['description'] = source_tariff.description
        return initial


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if 'formset' not in ctx:
            ctx['formset'] = TariffFormSet(prefix='tariff')

        return ctx

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = TariffFormSet(request.POST, prefix='tariff')

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()

        formset.instance = self.object
        formset.save()

        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form, formset):
        print(form.errors)
        print(formset.errors)
        return self.render_to_response(form=form, formset=formset)


    def get_success_url(self):
        return reverse_lazy('tariff')



class UpdateTariff(AdminpanelRestrictionMixin, UpdateView):
    required_section = 'tariff'

    model = Tariff
    template_name = 'create_tariff.html'
    form_class = TariffForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if 'formset' not in ctx:
            ctx['formset'] = TariffFormSet(instance=self.object, prefix='tariff')

        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        formset = TariffFormSet(request.POST, instance=self.object, prefix='tariff')

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()

        formset.instance = self.object
        formset.save()

        return HttpResponseRedirect(self.get_success_url())


    def form_invalid(self, form, formset):
        print(form.errors)
        print(formset.errors)
        return self.render_to_response(form=form, formset=formset)


    def get_success_url(self):
        return reverse_lazy('tariff')

class DeleteTariff(AdminpanelRestrictionMixin, DeleteView):
    required_section = 'tariff'

    model = Tariff
    success_url = reverse_lazy('tariff')



class ListCounter(ListView):
    model = Counters
    template_name = 'counter.html'
    context_object_name = 'counters'

class DetailListCounter(ListView):
    model = Counters
    template_name = "counter-list.html"
    context_object_name = 'counters'

    def get_queryset(self):
        queryset = super().get_queryset()

        apartment_query_set = self.request.GET.get('apartment_id')

        if apartment_query_set:
            queryset = queryset.filter(apartment__id=apartment_query_set)

        return queryset


class CreateCounter(CreateView):
    model = Counters
    template_name = 'create_counter.html'
    form_class = CounterForm


    def get_initial(self):
        initial = super().get_initial()

        apartment_id = self.request.GET.get('apartment_id')
        counter_id = self.request.GET.get('counter_id')

        if apartment_id:
            initial['apartment'] = apartment_id
            initial['create_time'] = datetime.now()

        if counter_id:
            service_initial = Counters.objects.filter(id=counter_id).first()

            if service_initial:
                initial['special_id'] = service_initial.special_id
                initial['service'] = service_initial.service


        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['all_house'] = House.objects.all()

        apartment_id = self.request.GET.get('apartment_id')

        if apartment_id:
            counter = Counters.objects.filter(apartment_id=apartment_id).first()

            if counter.apartment:
                ctx['current_apartment'] = counter.apartment
                ctx['current_section'] = counter.apartment.section
                ctx['current_house'] = counter.apartment.house

        return ctx


    def form_invalid(self, form):
        print(form.errors)

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        apartment_id = self.request.GET.get('apartment_id')

        if apartment_id:
            return reverse_lazy('counter-list') + f'?apartment_id={apartment_id}'
        return reverse_lazy('counter')



class UpdateCounter(UpdateView):
    model = Counters
    template_name = 'create_counter.html'
    form_class = CounterForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['all_house'] = House.objects.all()

        apartment_id = self.get_object()

        if apartment_id.apartment:
            ctx['current_section'] = apartment_id.apartment.section
            ctx['current_house'] = apartment_id.apartment.house

        return ctx

    def get_success_url(self):
        apartment_id = self.kwargs.get('pk')
        return reverse_lazy('counter-list') + f'?apartment_id={apartment_id}'


class DeleteCounter(DeleteView):
    model = Counters

    def get_success_url(self):
        apartment_id = self.kwargs.get('pk')
        return reverse_lazy('counter-list') + f'?apartment_id={apartment_id}'