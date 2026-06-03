from django.db import models

from src.adminpanel.models.UserChoise import Roles, Status
from src.common.models import Image
from src.users.models import User


# Create your models here.

class House(models.Model):
    name = models.CharField(max_length=20)
    adress = models.TextField()
    image_1 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='house_image_1')
    image_2 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='house_image_2')
    image_3 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='house_image_3')
    image_4 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='house_image_4')
    image_5 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='house_image_5')

    def __str__(self):
        return f"{self.name}"


class Section(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    section_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Storey(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    section_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"


class Worker(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_admin': True}, related_name='worker')
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    role = models.CharField(max_length=220)


class Apartment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    storey = models.ForeignKey(Storey, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) #і payment_account
    apartment_number = models.CharField(max_length=10)
    area = models.FloatField()

    def __str__(self):
        return f"{self.apartment_number}"


class Call_Master(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apartment_owner')
    master = models.ForeignKey(User, limit_choices_to={'is_admin': True}, on_delete=models.CASCADE, related_name='master')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    data_create = models.DateField()
    сonvenient_time = models.TimeField(null=True, blank=True)
    description = models.TextField()
    comment = models.TextField()
    role = models.CharField(choices=Roles.choices)
    status = models.CharField(choices=Status.choices, default=Status.choices[0][0])
