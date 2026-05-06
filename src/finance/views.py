from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView

from src.adminpanel.mixin import AdminpanelRestrictionMixin

from .models import Payment_Account
from .forms import PaymentAccountForm

from src.houses.models import House
# Create your views here.

class AccountList(ListView):
    model = Payment_Account
    template_name = 'account.html'
    context_object_name = 'accounts'

class AccountDetail(DetailView):
    model = Payment_Account
    template_name = 'show_account.html'
    context_object_name = 'account'

class CreateAccount(CreateView):
    model = Payment_Account
    template_name = 'create_account.html'
    form_class = PaymentAccountForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['all_house'] = House.objects.all()
        return ctx

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('account')


class UpdateAccount(UpdateView):
    model = Payment_Account
    template_name = 'create_account.html'
    form_class = PaymentAccountForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        account = self.get_object()

        ctx['all_house'] = House.objects.all()

        if account.apartment:
            ctx['current_apartment'] = account.apartment
            ctx['current_section'] = account.apartment.section
            ctx['current_house'] = account.apartment.house

        return ctx

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('account')


class DeleteAccount(DeleteView):
    model = Payment_Account
    success_url = reverse_lazy('account')