from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q # Фільтр щоб легше шукати, | - OR

from .models import User, Status, Image
from .forms import UserForm
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