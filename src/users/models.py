from django.db import models
from django.contrib.auth.models import AbstractUser
from src.adminpanel.models.UserChoise import Language, Role, Status, UserStatus
from django.core.validators import RegexValidator
from src.common.models import Image
# Create your models here.


phone_validator = RegexValidator(r'\+380\d{9}$')

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    language = models.CharField(max_length=4, choices=Language.choices, default=Language.choices[1][1], null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[phone_validator], unique=True)
    viber = models.CharField(max_length=20, null=True, blank=True, validators=[phone_validator])
    telegram = models.CharField(max_length=225, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    user_status = models.CharField(choices=UserStatus.choices, default=UserStatus.choices[1][1])
    main_image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='user_main_image', null=True, blank=True)
    user_id = models.BigIntegerField(unique=True, null=True, blank=True)

class Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_admin': True}, related_name='roles')
    role = models.CharField(max_length=40, choices=Role.choices, default=Language.choices[1][1])
    statistics = models.BooleanField(default=False)
    transaction = models.BooleanField(default=False)
    receipts = models.BooleanField(default=False)
    payment_account = models.BooleanField(default=False)
    apartments = models.BooleanField(default=False)
    house = models.BooleanField(default=False)
    messages = models.BooleanField(default=False)
    call_master = models.BooleanField(default=False)
    counters = models.BooleanField(default=False)
    site_control = models.BooleanField(default=False)
    services = models.BooleanField(default=False)
    tariff = models.BooleanField(default=False)
    role = models.BooleanField(default=False)
    users = models.BooleanField(default=False)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=225)
    text = models.TextField()
    date = models.DateTimeField()


class Call_Master(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    comment = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.choices[0][0])
