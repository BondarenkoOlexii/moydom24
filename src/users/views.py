from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from django.db.models import Q # Фільтр щоб легше шукати, | - OR

from .models import User, Image, Message, Call_Master
from .forms import UserForm, MessageForm, InviteMessage, CreateMaster
from src.houses.models import Apartment
from config_celery.celery_email_worker import send_invite_email, app

# Create your views here.



class ListUser(ListView):
    model = User
    template_name = 'user.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()

        search_id_query = self.request.GET.get('UserSearch[uid]', '')
        search_name_query = self.request.GET.get('UserSearch[searchFullname]', '')
        search_phone_query = self.request.GET.get('UserSearch[searchPhone]', '')
        search_email_query = self.request.GET.get('UserSearch[email]', '')

        if search_name_query:
            queryset = queryset.filter(user_id__icontains=search_id_query)

        if search_name_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_name_query) |
                Q(middle_name__icontains=search_name_query) |
                Q(last_name__icontains=search_name_query)
            )

        if search_phone_query:
            queryset = queryset.filter(phone_number__icontains=search_phone_query)

        if search_email_query:
            queryset = queryset.filter(email__icontains=search_email_query)

        return queryset

    def get_context_data(self, **kwargs): # Щоб все не зникло після перезавантаження
        contex = super().get_context_data(**kwargs)
        contex['filter'] = self.request.GET
        return contex


class CreateUser(CreateView):
    model = User
    template_name = 'create_user.html'
    form_class = UserForm

    def form_valid(self, form):
        print("ФОРМА ВАЛІДНА")
        self.object = form.save(commit=False)

        img_obj = form.cleaned_data.get('main_image')

        if img_obj:

            upload_img = Image.objects.create(photo=img_obj)
            self.object.main_image = upload_img

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form):
        print(form.errors)

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('user')
class UpdateUser(UpdateView):
    model = User
    template_name = 'create_user.html'
    form_class = UserForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        img_obj = form.cleaned_data.get('main_image')

        if img_obj:
            upload_img = Image.objects.create(photo=img_obj)
            self.object.main_image = upload_img

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('user')
class DeleteUser(DeleteView):
    model = User
    success_url = reverse_lazy('user')


class CreateMessage(CreateView):
    model = Message
    template_name = 'new_message.html'
    form_class = MessageForm

    def form_valid(self, form):
        print("ФОРМА ВАЛІДНА")

        data = form.cleaned_data


        print(data)

        apartments = Apartment.objects.all()

        if data.get('apartment'):
            apartments = apartments.filter(id=data['apartment'].id)

        elif data.get('storey'):
            apartments = apartments.filter(storey=data['storey'])

        elif data.get('section'):
            apartments = apartments.filter(section=data['section'])

        elif data.get('house'):
            apartments = apartments.filter(house=data['house'])

        owners = apartments.values_list('owner', flat=True)
        print(owners)

        if not any([data.get('house'), data.get('section'), data.get('storey'), data.get('apartment')]):
            owners = User.objects.values_list('name', flat=True)

        list_of_message = []
        for obj in owners:
            if obj:
                list_of_message.append(
                    Message(
                        theme=form.cleaned_data['theme'],
                        text=form.cleaned_data['text'],
                        user_id=obj
                    )
                )
        Message.objects.bulk_create(list_of_message) # Добавляємо пачкою

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


    def get_success_url(self):
        return reverse('user')


class EmailInvite(FormView):
    form_class = InviteMessage
    template_name = 'invite_message.html'
    success_url = 'invite_message'

    def form_valid(self, form):
        email_to = form.cleaned_data.get('email')
        print(f'Дані отримав {email_to}')

        invite_task = send_invite_email.delay('ABC', 'message', 'mayoright01@gmail.com', email_to)

        print('Дані надіслав')

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('user')




class ListMessage(ListView):
    model = Message
    template_name = 'messages.html'
    context_object_name = 'messages'

class SpecificMessage(DetailView):
    model = Message
    template_name = 'current_message.html'
    context_object_name = 'view'

class DeleteMessage(DeleteView):
    model = Message
    success_url = reverse_lazy('messages')




class ListMasterRequest(ListView):
    model = Call_Master
    template_name = 'master-request.html'
    context_object_name = 'masters'


class NewMasterRequest(CreateView):
    model = Call_Master
    template_name = 'new-master-request.html'



class MasterList(ListView):
    model = User
    template_name = 'masters.html'
    context_object_name = 'form'

class CreateMaster(CreateView):
    model = User
    template_name = 'new_master.html'
    form_class = CreateMaster


    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('master-list')
