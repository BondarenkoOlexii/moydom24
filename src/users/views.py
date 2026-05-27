from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView, TemplateView
from ajax_datatable.views import AjaxDatatableView

from .models import User, Image, Message, Role
from .forms import UserForm, MessageForm, InviteMessage, CreateMasterForm
from src.houses.models import Apartment, House
from src.adminpanel.models.UserChoise import UserStatus
from config_celery.celery_email_worker import send_invite_email, app
from src.adminpanel.mixin import AdminpanelRestrictionMixin
# Create your views here.



class ListUser(AdminpanelRestrictionMixin, TemplateView):
    required_section = 'apartments_owner'

    template_name = 'user.html'


class UserDatatableView(AjaxDatatableView):
    model = User
    title = "Пользователи"
    initial_order = [['user_id', 'asc']]

    length_menu = [[10, 20, 50, 100], [10, 20, 50, 100]]

    column_defs = [
        {'name': 'id', 'searchable': False, 'visible': False},
        {'name': 'user_id', 'title': 'ID', 'visible': True, 'searchable': True},
        {'name': 'first_name', 'title': 'ФИО', 'visible': True, 'searchable': True},
        {'name': 'phone_number', 'title': 'Телефон', 'visible': True, 'searchable': True},
        {'name': 'email', 'title': 'Emain', 'visible': True, 'searchable': True},
        {'name': 'house_name', 'title': 'Доми', 'visible': True, 'placeholder': True, 'choices': [('', 'Выберите дом')], 'searchable': True, 'orderable': False},
        {'name': 'apartment_num', 'title': 'Квартири', 'visible': True, 'placeholder': True, 'choices': [('', 'Выберите квартиру')], 'searchable': True, 'orderable': False},
        {'name': 'date_joined', 'title': 'Добавлен', 'visible': True, 'searchable': True},
        {'name': 'user_status', 'title': 'Статус', 'visible': True, 'searchable': False, 'choices': UserStatus.choices, 'autofilter': True},
        {'name': 'actions', 'title': '', 'visible': True, 'searchable': False, 'orderable': False},
    ]

    def get_column_defs(self, request):
        column_defs = super().get_column_defs(request)

        for col in column_defs:
            if col['name'] == 'house_name':
                col['choices'] = [('', 'Выберите дом')] + [(h.id, h.name) for h in House.objects.all()]

        return column_defs

    def customize_row(self, row, obj):
        apt = obj.apartment_set.first() if hasattr(obj, 'apartment_set') else None

        row['house_name'] = apt.house.name if apt and apt.house else '—'
        row['apartment_num'] = f"№ {apt.apartment_number}" if apt else '—'



        edit_url = reverse('update_user', kwargs={'pk': obj.id})
        delete_url = reverse('delete_user', kwargs={'pk': obj.id})

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

    def filter_queryset(self, params, qs):
        # 1. ПЕРЕХОПЛЮЄМО ЗНАЧЕННЯ НАШИХ ФІЛЬТРІВ (Будинок і Квартира)
        house_val = None
        apt_val = None
        clean_links = []

        for col in params.get('column_links', []):
            if col.name == 'house_name':
                house_val = col.search_value
            elif col.name == 'apartment_num':
                apt_val = col.search_value
            else:
                # Зберігаємо всі інші колонки (щоб пошук по ФІО і Телефону працював)
                clean_links.append(col)

        # 2. Ховаємо наші кастомні колонки від бібліотеки, щоб вона не зламала QuerySet!
        params['column_links'] = clean_links

        # 3. Викликаємо стандартний пошук
        qs = super().filter_queryset(params, qs)

        # 4. Вручну застосовуємо фільтрацію по базі даних
        # Зверни увагу: я використовую 'apartment', бо так було в твоїй помилці раніше
        if house_val:
            qs = qs.filter(apartment__house_id=house_val).distinct()
        if apt_val:
            qs = qs.filter(apartment__id=apt_val).distinct()

        return qs




class CreateUser(AdminpanelRestrictionMixin, CreateView):
    required_section = 'apartments_owner'

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

        self.object.set_password(form.cleaned_data.get('password'))
        self.object.username = f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('middle_name')} {form.cleaned_data.get('last_name')}"

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form):
        print(form.errors)

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('user')


class BasicUpdateUser(UpdateView):
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


class UpdateUser(AdminpanelRestrictionMixin, BasicUpdateUser):
    required_section = 'apartments_owner'



class DeleteUser(AdminpanelRestrictionMixin, DeleteView):
    required_section = 'apartments_owner'

    model = User
    success_url = reverse_lazy('user')


class CreateMessage(AdminpanelRestrictionMixin, CreateView):
    required_section = 'messages'

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


class EmailInvite(AdminpanelRestrictionMixin, FormView):
    required_section = 'messages'

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




class ListMessage(AdminpanelRestrictionMixin, ListView):
    required_section = 'messages'

    model = Message
    template_name = 'messages.html'
    context_object_name = 'messages'

class SpecificMessage(AdminpanelRestrictionMixin, DetailView):
    required_section = 'messages'

    model = Message
    template_name = 'current_message.html'
    context_object_name = 'view'

class DeleteMessage(AdminpanelRestrictionMixin, DeleteView):
    required_section = 'messages'

    model = Message
    success_url = reverse_lazy('messages')


class MasterList(AdminpanelRestrictionMixin, TemplateView):
    required_section = 'users'

    template_name = 'masters.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        role_list = User.objects.prefetch_related('roles')

        context['roles'] = role_list

        return context


class MasterDatatableView(AjaxDatatableView):
    model = User
    title = "Мастера"
    initial_order = [['id', 'asc']]

    length_menu = [[10, 20, 50, 100], [10, 20, 50, 100]]

    column_defs = [
        # {'name': 'id', 'searchable': False, 'visible': False},
        {'name': 'id', 'title': 'ID', 'visible': True, 'searchable': True},
        {'name': 'first_name', 'title': 'ФИО', 'visible': True, 'searchable': True},

        {'name': 'role', 'title': 'Роли', 'visible': True, 'placeholder': True, 'choices': [('', 'Выберите роль')], 'searchable': True, 'orderable': False},

        {'name': 'phone_number', 'title': 'Телефон', 'visible': True, 'searchable': True},
        {'name': 'email', 'title': 'Emain', 'visible': True, 'searchable': True},
        {'name': 'user_status', 'title': 'Статус', 'visible': True, 'searchable': False, 'choices': UserStatus.choices, 'autofilter': True},
        {'name': 'actions', 'title': '', 'visible': True, 'searchable': False, 'orderable': False},
    ]


    def get_column_defs(self, request): # Тут заповнюємо список ролей
        defs = super().get_column_defs(request)

        for item in defs:
            if item['name'] == 'role':
                item['choices'] = [('', '')] + [(r.id, r.role) for r in Role.objects.all()]

        return defs


    def customize_row(self, row, obj):
        master_role = obj.roles.first() if hasattr(obj, 'roles') else None

        row['role'] = master_role.get_role_display() if master_role else '-'


        status_text = obj.get_user_status_display() if obj.user_status else '-'

        status_color = obj.get_color_status() if hasattr(obj, 'get_color_status') else 'label-danger'

        row['user_status'] = f'<span class="label {status_color}">{status_text}</span>'

        #row['detail_url'] = reverse('') - детейл для мастера



        edit_url = reverse('master-list-update', kwargs={'pk': obj.id})
        delete_url = reverse('master-list-delete', kwargs={'pk': obj.id})

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

    def filter_queryset(self, params, qs):
        role_val = None
        clean_links = []

        for item in params.get('column_links', []):
            if item.name == 'role':
                role_val = item.search_value
            else:
                clean_links.append(item)

        params['column_links'] = clean_links
        qs = super().filter_queryset(params, qs)

        if role_val:
            qs = qs.filter(roles__id=role_val).distinct()

        return qs

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset(request)
        # Повертаємо тільки тих користувачів, у яких є хоча б одна роль (тобто вони майстри)
        # Або можна фільтрувати по qs.filter(is_staff=True), залежить від твоєї логіки
        return qs.filter(is_staff=True).distinct().prefetch_related('roles')



class CreateMaster(AdminpanelRestrictionMixin, CreateView):
    required_section = 'users'

    model = User
    template_name = 'new_master.html'
    form_class = CreateMasterForm


    def form_valid(self, form):

        role_data = form.cleaned_data['role_select']

        form.cleaned_data.pop('role_select', None) # Зберігаємо і видаляємо поле якого нема в User
        form.cleaned_data.pop('password_confirm', None)
        form['username'] = form.cleaned_data['first_name']
        form.cleaned_data['is_admin'] = True

        user_obj = User.objects.create(**form.cleaned_data) # Дуже удобно, зберігаємо все і сразу а не прописуємо кожне поле окремо

        role_data = Role.objects.create(user=user_obj, role=role_data)

        return super().form_valid(form)


    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('master-list')


class UpdateMaster(AdminpanelRestrictionMixin, UpdateView):
    required_section = 'users'

    model = User
    template_name = 'new_master.html'
    form_class = CreateMasterForm
    success_url = 'master-list'

    def get(self, request, *args, **kwargs):
        # 1. Дістаємо об'єкт з бази (наприклад, юзера з ID=5)
        self.object = self.get_object()

        print("\n=== ДЕБАГ GET-ЗАПИТУ ===")
        print(f"1. Кого ми дістали з бази: {self.object.username} (ID: {self.object.id})")
        print(f"2. Що в нього записано в полі first_name у БАЗІ: '{self.object.first_name}'")
        print(f"3. Що в нього записано в полі email у БАЗІ: '{self.object.email}'")

        # 2. Просимо Django створити форму і передати їй цього юзера
        form = self.get_form()

        #print(f"4. Що форма отримала в поле first_name: '{form['first_name'].value()}'")
        print("========================\n")

        # 3. Відмальовуємо сторінку
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)



    def get_initial(self):
        initial = super().get_initial()

        user = self.get_object()

        current_role = user.roles.first()

        if current_role:
            initial['role_select'] = current_role

        return initial

    def form_valid(self, form):
        user = form.save(commit=False)

        user.cleaned_data['username'] = form.cleaned_data['first_name']
        user.cleaned_data['is_admin'] = True

        user.save()

        role_data = form.cleaned_data['role_select']

        Role.objects.update_or_create(
            user=user,
            role=role_data
        )

        return super().form_valid(form)


class DeleteMaster(AdminpanelRestrictionMixin, DeleteView):
    required_section = 'users'

    model = User
    success_url = reverse_lazy('master-list')
