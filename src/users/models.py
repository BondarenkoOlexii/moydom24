from django.db import models
from django.contrib.auth.models import AbstractUser
from src.adminpanel.models.UserChoise import Language, Roles, Status, UserStatus
from django.core.validators import RegexValidator
from src.common.models import Image
# Create your models here.


phone_validator = RegexValidator(r'\+380\d{9}$')

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    language = models.CharField(max_length=4, choices=Language.choices, default=Language.choices[1][0], null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[phone_validator], unique=True)
    viber = models.CharField(max_length=20, null=True, blank=True, validators=[phone_validator])
    telegram = models.CharField(max_length=225, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    user_status = models.CharField(choices=UserStatus.choices, default=UserStatus.choices[1][0])
    main_image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='user_main_image', null=True, blank=True)
    user_id = models.BigIntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_color_status(self):
        if self.user_status == 'active':
            return 'label-success'
        elif self.user_status == UserStatus.new:
            return 'label-warning'
        return 'label-danger'


class Role(models.Model):
    user = models.ManyToManyField(User, limit_choices_to={'is_admin': True}, related_name='roles')
    role = models.CharField(max_length=40, choices=Roles.choices, default=Language.choices[1][1])
    statistics = models.BooleanField(default=False) # Статистика
    transaction = models.BooleanField(default=False) # Касса
    receipts = models.BooleanField(default=False) # Квитанции
    payment_account = models.BooleanField(default=False) # Лицевой счет
    apartments_owner = models.BooleanField(default=False) # Владелци квартир
    apartments = models.BooleanField(default=False) # Квартири
    house = models.BooleanField(default=False) # Дома
    messages = models.BooleanField(default=False) # Сообщения
    call_master = models.BooleanField(default=False) # Заявка мастера
    counters = models.BooleanField(default=False) # Счетчики
    site_control = models.BooleanField(default=False) # Управления сайтом
    services = models.BooleanField(default=False) # Услуги
    tariff = models.BooleanField(default=False) # Таріфи
    role_list = models.BooleanField(default=False) # Роли
    users = models.BooleanField(default=False) # Пользователи
    payment_data = models.BooleanField(default=False) # Платежни реквезити
    transaction_propose = models.BooleanField(default=False)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='taker')
    theme = models.CharField(max_length=225)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
