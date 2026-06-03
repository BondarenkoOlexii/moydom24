from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from ajax_datatable.views import AjaxDatatableView
from datetime import date

from src.adminpanel.mixin import AdminpanelRestrictionMixin

from .models import Payment_Account, Invoice, ThoughInvoiceService, Cash_Register
from .forms import PaymentAccountForm, InvoiceForm, InvoiceServiceFormSet, CashRegisterForm

from src.houses.models import House
from src.adminpanel.models.FinanceChoise import InvoiceChoise
from src.users.models import User
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

    boolean_choices = [
        (True, 'Проведена'),
        (False, 'Не проведена')
    ]


    column_defs = [

        {'name': 'id', 'visible': True, 'searchable': False},
        {'name': 'type', 'title': 'Статус', 'visible': True, 'searchable': True, 'choices': InvoiceChoise.choices},
        {'name': 'create_time', 'visible': True, 'searchable': True},
        {'name': 'period_start', 'title': 'Месяц', 'searchable': True, 'placeholder': 'Месяц'},
        {'name': 'payment_account__apartment__apartment_number', 'title': 'Квартири', 'visible': True, 'searchable': True},
        {'name': 'payment_account__apartment__owner__first_name', 'title': 'Владелец', 'visible': True, 'placeholder': True, 'searchable': True, 'orderable': True, 'choices': [('', '')]},
        {'name': 'status', 'title': 'Проведена', 'visible': True, 'searchable': True, 'choices': boolean_choices},
        {'name': 'actions', 'title': '', 'visible': True, 'searchable': False, 'orderable': False},
    ]

    def get_column_defs(self, request):
        column_defs = super().get_column_defs(request)

        for col in column_defs:
            if col['name'] == 'payment_account__apartment__owner__first_name':
                col['choices'] = [(h.first_name, f"{h.first_name} {h.last_name}") for h in User.objects.all()]

        return column_defs

    def customize_row(self, row, obj):
        if obj.payment_account and obj.payment_account.apartment and obj.payment_account.apartment.owner:
            owner = obj.payment_account.apartment.owner
            row['payment_account__apartment__owner__first_name'] = f"{owner.first_name} {owner.last_name}"
        else:
            row['payment_account__apartment__owner__first_name'] = "—"

        if obj.payment_account and obj.payment_account.apartment.apartment_number:
            apartment = obj.payment_account.apartment
            row['payment_account__apartment__apartment_number'] = f"{apartment.apartment_number} {apartment.house.name}"

        if obj.period_start:
            MONTHS_UA = {
                1: 'Січень', 2: 'Лютий', 3: 'Березень', 4: 'Квітень',
                5: 'Травень', 6: 'Червень', 7: 'Липень', 8: 'Серпень',
                9: 'Вересень', 10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'
            }

            try:
                month = MONTHS_UA[obj.period_start.month]
                row['period_start'] = f"{month} {obj.period_start.year}"
            except AttributeError:
                pass

        edit_url = reverse('invoice_update', kwargs={'pk': obj.id})
        delete_url = reverse('invoice_delete', kwargs={'pk': obj.id})

        row['actions'] = f'''
                    <div class="btn-group pull-right">
                       <a class="btn btn-default btn-sm" href="{edit_url}" title="Редагувати" data-toggle="tooltip">
                           <i class="fa fa-pencil"></i>
                       </a>

                       <a class="btn btn-default btn-sm" href="{delete_url}" title="Видалити" data-toggle="tooltip">
                          <i class="fa fa-trash"></i>
                       </a>
                    </div>
                '''

        row['DT_RowAttr'] = {
            'data-href': reverse('invoice_detail', kwargs={'pk': obj.id}),
            'style': 'cursor: pointer'
        }
        return row


class DetailInvoice(DetailView):
    model = Invoice
    template_name = 'show_invoice.html'
    context_object_name = 'invoice'
    success_url = reverse_lazy('invoice')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['formset'] = ThoughInvoiceService.objects.filter(invoice=self.kwargs.get('pk'))

        return ctx

class CreateInvoice(CreateView):
    model = Invoice
    template_name = 'create_invoice.html'
    form_class = InvoiceForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.request.POST:
            ctx['formset'] = InvoiceServiceFormSet(self.request.POST, prefix='invoiceservice_set')
        else:
            ctx['formset'] = InvoiceServiceFormSet(prefix='invoiceservice_set')

        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None

        form = self.get_form()
        formset = InvoiceServiceFormSet(request.POST, instance=self.object, prefix='invoiceservice_set')

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

        return self.render_to_response(self.get_context_data(form=form, formset=formset))


    def get_success_url(self):
        return reverse_lazy('invoice')


class UpdateInvoice(UpdateView):
    model = Invoice
    template_name = 'create_invoice.html'
    form_class = InvoiceForm


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        invoice = self.object

        if self.request.POST:
            ctx['formset'] = InvoiceServiceFormSet(self.request.POST, instance=self.object, prefix='invoiceservice_set')
        else:
            ctx['formset'] = InvoiceServiceFormSet(instance=self.object, prefix='invoiceservice_set')

        ctx['apartment'] = invoice.payment_account.apartment
        ctx['house'] = invoice.payment_account.apartment.house
        ctx['section'] = invoice.payment_account.apartment.section

        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        post_data = request.POST.copy()
        text_payment_account = post_data.get('payment_account')

        if text_payment_account and not str(text_payment_account).isdigit():
            try:
                account = Payment_Account.objects.get(bank_book=text_payment_account)
                post_data['payment_account'] = account.id
            except Payment_Account.DoesNotExist:
                pass

        form = self.form_class(post_data, instance=self.object)
        formset = InvoiceServiceFormSet(post_data, instance=self.object, prefix='invoiceservice_set')

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)


    def form_valid(self, form, formset):
        self.object = form.save(commit=False)

        total_price = 0

        for i in formset:
            indicator = i.cleaned_data.get('indicator')
            measurement_price = i.cleaned_data.get('measurement_price')
            iprice = int(indicator) * int(measurement_price)

            i.instance.price = iprice
            total_price += iprice
        self.object.total_amount = total_price

        form.save()

        formset.instance = self.object
        print(formset)
        formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        print(form.errors)
        print(formset.errors)

        return self.render_to_response(self.get_context_data(form=form, formset=formset))


    def get_success_url(self):
        return reverse_lazy('invoice')


class DeleteInvoice(DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice')


class ListAccountTransaction(TemplateView):
    template_name = 'account-transaction.html'


class AccountTransactionDatatableView(AjaxDatatableView):
    model = Cash_Register
    title = 'Касса'
    initial_order = [['unique_id', 'desc']]

    length_menu = [[10, 20, 50, 100], [10, 20, 50, 100]]

    boolean_choise = [
        (True, ''),
        (False, '')
    ]

    column_defs = [
        {'name': 'id', 'visible': False, 'searchable': False},
        {'name': 'unique_id', 'title': '№', 'visible': True, 'searchable': True},
        {'name': 'create_time', 'title': 'Дата', 'visible': True, 'searchable': True},
        {'name': 'status', 'title': 'Статус', 'visible': True, 'searchable': True, 'choices': boolean_choise},
        {'name': 'type', 'title': 'Тип платежа', 'visible': True, 'searchable': True},
        {'name': 'account__apartment__owner__first_name', 'title': 'Владелец', 'visible': True, 'searchable': True, 'placeholder': True, 'choices': [('', '')]},
        {'name': 'account', 'title': 'Лицевой счет', 'visible': True, 'searchable': True},
        {'name': 'artical', 'title': 'Приход/расход', 'visible': True, 'searchable': True},
        {'name': 'sum', 'title': 'Сумма (грн)', 'visible': True, 'searchable': True},
        {'name': 'actions', 'title': '', 'visible': True, 'searchable': False, 'orderable': False},

    ]

    def get_column_defs(self, request):
        column_defs = super().get_column_defs(request)

        for col in column_defs:
            if col['name'] == 'account__apartment__owner__first_name':
                col['choices'] = [(h.first_name, f"{h.first_name} {h.last_name}") for h in User.objects.all()]

        return column_defs


    def customize_row(self, row, obj):
        if obj.account and obj.account.apartment and obj.account.apartment.owner:
            owner = obj.account.apartment.owner
            row['account__apartment__owner__first_name'] = f"{owner.first_name} {owner.last_name}"
        else:
            row['account__apartment__owner__first_name'] = "—"



        edit_url = reverse('account-transaction_update', kwargs={'pk': obj.id})
        delete_url = reverse('account-transaction_delete', kwargs={'pk': obj.id})

        row['actions'] = f'''
                    <div class="btn-group pull-right">
                       <a class="btn btn-default btn-sm" href="{edit_url}" title="Редагувати" data-toggle="tooltip">
                           <i class="fa fa-pencil"></i>
                       </a>

                       <a class="btn btn-default btn-sm" href="{delete_url}" title="Видалити" data-toggle="tooltip">
                          <i class="fa fa-trash"></i>
                       </a>
                    </div>
                '''

class DetailAccountTransaction(DetailView):
    model = Cash_Register
    template_name = 'show_account-transaction.html'

class CreateAccountTransaction(CreateView):
    model = Cash_Register
    template_name = 'create_account-transaction.html'
    form_class = CashRegisterForm

    def get_initial(self):
        initial = super().get_initial()



    def form_valid(self, form):
        self.object = form.save(commit=False)

        cash_register_type = self.request.GET.get('type')

        if cash_register_type == 'in':
            self.object.type = 'arrival'
        else:
            self.object.type = 'expense'

        form.save()

        return HttpResponseRedirect(reverse_lazy('account-transaction'))

    def form_invalid(self, form):
        print(form.errors)

        return self.render_to_response(self.get_context_data())


class UpdateAccountTransaction(UpdateView):
    model = Cash_Register
    template_name = 'create_account-transaction.html'
    form_class = CashRegisterForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        cash_register_type = self.request.GET.get('type')

        if cash_register_type == 'in':
            self.object.type = 'arrival'
        else:
            self.object.type = 'expense'

        form.save()

        return HttpResponseRedirect(reverse_lazy('account-transaction'))

    def form_invalid(self, form):
        print(form.errors)

        return self.render_to_response(self.get_context_data())


class DeleteAccountTransaction(DeleteView):
    model = Cash_Register
    success_url = reverse_lazy('account-transaction')