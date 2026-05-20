from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.

from src.site_control.models import Main_Page, About_Page, Contact_Page, Additional_Block, Additional_File
from src.users.models import User
from src.users.forms import UserForm
from src.houses.models import Apartment
from src.common.models import Image
from src.finance.models import Payment_Account
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

        ctx['object'] = User.objects.get(id=user_id)

        ctx['apartments'] = Apartment.objects.filter(owner=user_id)

        ctx['payment_account'] = Payment_Account.objects.filter(apartment__owner=user_id).first()

        return ctx

class UpdateUserCabinet(CreateView):
    model = User
    template_name = ''
    form_class = UserForm

    def get_object(self, queryset=None):
        user = self.request.user.user_id
        try:
            cabinet = Main_Page.objects.get(user_id=user)
            return cabinet
        except(AttributeError, User.DoesNotExist):
            return None

    def form_valid(self, form):

        self.object = form.save(commit=False)

        img_obj = form.cleaned_data.get('main_image')

        if img_obj:
            upload_img = Image.objects.create(photo=img_obj)
            self.object.main_image = upload_img

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('user')
