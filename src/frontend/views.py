from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from ajax_datatable.views import AjaxDatatableView
from django.db import transaction as db_transaction
# Create your views here.

from src.site_control.models import Main_Page, About_Page, Contact_Page, Additional_Block, Additional_File
from src.users.models import User, Message
from src.users.forms import UserForm
from src.houses.models import Apartment, Call_Master
from src.common.models import Image
from src.finance.models import Payment_Account, Tariff, Invoice, ThoughInvoiceService, Transaction, Cash_Register
from src.users.views import BasicUpdateUser
from .forms import CabinetCallMaster, CustomLoginForm, PaymentMethodChoise


class CustomUserLogin(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('view_user_cabinet')

    def form_valid(self, form):

        responce = super().form_valid(form)

        remember_me = form.cleaned_data['remember_me']

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(None)
        return responce

    def form_invalid(self, form):
        print("====== УВАГА! ФОРМА НЕ ВАЛІДНА ======")
        print("Помилки полів:", form.errors)
        print("Глобальні помилки (тут зазвичай про неправильний пароль):", form.non_field_errors())
        print("=======================================")
        return super().form_invalid(form)


class CustomUserLogout(LogoutView):

    def get_success_url(self):
        return reverse_lazy('main')


class CustomAdminLogin(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_admin:
            return reverse_lazy('dashboard')
        return reverse_lazy('main')

    def form_valid(self, form):

        responce = super().form_valid(form)

        remember_me = form.cleaned_data['remember_me']

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(None)
        return responce


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['object'] = Main_Page.objects.first()

        ctx['contact'] = Contact_Page.objects.first()

        ctx['additional_block'] = Additional_Block.objects.filter(main_page=1)
        return ctx


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['object'] = About_Page.objects.first()

        ctx['additional_block'] = Additional_Block.objects.filter(about_page=1)

        ctx['additional_files'] = Additional_File.objects.all()

        return ctx


class ServiceView(ListView):
    model = Additional_Block
    template_name = 'services.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['objects'] = Additional_Block.objects.filter(main_page=None, about_page=None)

        return ctx


class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['object'] = Contact_Page.objects.first()

        return ctx


########################################################################################################################

class ListCabinetUser(ListView):
    model = User
    template_name = 'view_cabinet.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user_id = self.request.user.id

        ctx['object'] = User.objects.filter(id=user_id).first()

        ctx['apartments'] = Apartment.objects.filter(owner=user_id)

        ctx['payment_account'] = Payment_Account.objects.filter(apartment__owner=user_id).first()

        return ctx


class UpdateUserCabinet(BasicUpdateUser):

    def get_object(self, queryset=None):
        user = self.request.user.id
        print(user)
        try:
            cabinet = User.objects.get(id=user)
            return cabinet
        except(AttributeError, User.DoesNotExist):
            return None


class ListCabinetMasterRequest(ListView):
    model = Call_Master
    template_name = 'user_list_master.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user = self.request.user.id

        ctx['objects'] = Call_Master.objects.filter(user=user)

        return ctx


class CreateCabinetMasterRequest(CreateView):
    model = Call_Master
    template_name = 'user_call_master.html'
    form_class = CabinetCallMaster


class ListCabinetMessages(ListView):
    model = Message
    template_name = "cabinet_messages.html"


class ListCabinetTariff(ListView):
    model = Tariff
    template_name = 'cabinet_tariff.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        payment_account = Payment_Account.objects.filter(apartment=self.request.GET.get('apartment')).first()

        invoice = Invoice.objects.filter(payment_account=payment_account)

        ctx['objects'] = ThoughInvoiceService.objects.filter(invoice__in=invoice)

        ctx['apartment'] = Apartment.objects.filter(id=self.request.GET.get('apartment')).first()
        return ctx


class ListCabinetInvoice(TemplateView):
    template_name = 'cabinet_invoice.html'


class CabinetInvoiceDatatableView(AjaxDatatableView):
    model = Invoice
    title = 'Квитанції Користувача'
    initial_order = [['invoice_unique_id', "desc"]]

    length_menu = [[10, 20, 50, 100], [10, 20, 50, 100]]

    boolean_choices = [
        (True, 'Проведена'),
        (False, 'Не проведена')
    ]

    column_defs = [
        {'name': 'id', 'title': '№', 'visible': False, 'searchable': False},
        {'name': 'invoice_unique_id', 'visible': True, 'searchable': True},
        {'name': 'create_time', 'visible': True, 'searchable': True},
        {'name': 'status', 'title': 'Проведена', 'visible': True, 'searchable': True, 'choices': boolean_choices},
        {'name': 'total_amount', 'visible': True, 'searchable': False}

    ]

    def get_initial_queryset(self, request=None):

        apartment_id = self.request.GET.get("apartment")

        return Invoice.objects.filter(payment_account__apartment=apartment_id,
                                      payment_account__apartment__owner=request.user)

    def customize_row(self, row, obj):
        apartment_id = self.request.GET.get('apartment')

        base_url = reverse('cabinet_invoice_view', kwargs={'pk': obj.pk})

        row['DT_RowAttr'] = {
            'data-url': f"{base_url}?apartment={ apartment_id }"
        }


class CabinetInvoiceView(DetailView):
    model = Invoice
    template_name = 'cabinet_invoice_view.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        print(pk)

        ctx['services'] = ThoughInvoiceService.objects.filter(invoice_id=pk)

        return ctx


class CabinetInvoicePaymentMethod(FormView):
    template_name = 'payment_method.html'
    form_class = PaymentMethodChoise

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        apartment = self.request.GET.get("apartment")

        with db_transaction.atomic():

            cash_register = Cash_Register.objects.create(
                account=get_object_or_404(Payment_Account, apartment=apartment),
                type='arrival',
                sum=amount
            )

            transaction_model = Transaction.objects.create(
                cash_register=cash_register,
                status='conducted',
                amount=amount
            )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return f"{reverse('list_user_invoice')}?apartment={self.request.GET.get('apartment')}"


