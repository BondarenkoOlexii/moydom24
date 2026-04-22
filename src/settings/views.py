from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.http import JsonResponse


from .models import PaymentInfo, TransactionPurpose, Service, Measurement, Tariff
from src.users.models import Role
from .forms import PaymentInfoForm, TransactionPurposeForm, ServiceFormSet, ServiceForm, MeasurementFormSet,\
    MeasurementForm, TariffForm, TariffFormSet, RoleForm
# Create your views here.




class AdminpanelRestrictionMixin(PermissionRequiredMixin):
    app_list = ['src.adminpanel', 'src.authorization', 'src.finance', 'src.houses', 'src.settings', 'src.site_control',
                'src.users']

    user = request.user.id

    user_access = Role.objects.filter(user=user)





class RoleView(ListView):
    model = Role
    template_name = 'role.html'
    # form_class = RoleForm
    context_object_name = 'roles'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if 'form' not in ctx:
            ctx['form'] = RoleForm()

            ctx['roles_for_forms'] = [
                RoleForm(instance=role) for role in ctx['roles']
            ]

        return ctx

    def post(self, request, *args, **kwargs):
        print(request.POST)

    def get_success_url(self):
        return reverse('role')

class PaymentInfoCreate(CreateView):
    model = PaymentInfo
    template_name = 'pay-company.html'
    form_class = PaymentInfoForm
    success_url = 'pay-company'


class TransactionProposeList(ListView):
    model = TransactionPurpose
    template_name = 'transaction-purpose.html'
    context_object_name = 'form'

class TransactionProposeCreate(CreateView):
    model = TransactionPurpose
    template_name = 'transaction-purpose_create.html'
    form_class = TransactionPurposeForm
    success_url = reverse_lazy('transaction-purpose')

class TransactionProposeUpdate(UpdateView):
    model = TransactionPurpose
    template_name = 'transaction-purpose_create.html'
    form_class = TransactionPurposeForm
    success_url = 'transaction-purpose'

class TransactionProposeDelete(DeleteView):
    model = TransactionPurpose
    success_url = reverse_lazy('transaction-purpose')




class ServiceView(TemplateView):
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


class TariffList(ListView):
    model = Tariff
    template_name = 'tariff.html'
    context_object_name = 'form'


class CreateTariff(CreateView):
    model = Tariff
    template_name = 'create_tariff.html'
    form_class = TariffForm

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



class UpdateTariff(UpdateView):
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

class DeleteTariff(DeleteView):
    model = Tariff
    success_url = reverse_lazy('tariff')