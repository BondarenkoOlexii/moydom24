from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from ajax_datatable.views import AjaxDatatableView

from src.adminpanel.mixin import AdminpanelRestrictionMixin

from .models import Payment_Account, Invoice
from .forms import PaymentAccountForm, InvoiceForm

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



class ListInvoice(TemplateView):
    #model = Invoice
    template_name = 'invoice.html'
    #context_object_name = 'invoices'


class InvoiceDatatableView(AjaxDatatableView):
    model = Invoice
    title = 'Квитанції'
    initial_order = [['id', "desc"]] # То як буде відфільтрований список при першому заході по id від нового до старого

    length_menu = [[10, 20, 50, 100], [10, 20, 50, 100]] # Пагінація

    column_defs = [
        {'name': 'id', 'visible': True, 'searchable': False},
        {'name': 'status', 'visible': True, 'searchable': False},
        {'name': 'create_time', 'visible': True, 'searchable': False},
        {'name': 'service', 'foreign_field': 'service__service', 'visible': True, 'searchable': True, 'choices': True}, # це для Foreign Key і випадаючого списка (choices: True якщо в нас є вбудований choise в моделі)

    ]

class CreateInvoice(CreateView):
    model = Invoice
    template_name = 'create_invoice.html'
    form_class = InvoiceForm

