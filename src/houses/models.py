from django.db import models
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


class Section(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    section_number = models.CharField(max_length=10, null=True, blank=True)


class Storey(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    section_number = models.CharField(max_length=10)

class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_admin': True}, related_name='worker')
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)


class Apartment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    storey = models.ForeignKey(Storey, on_delete=models.CASCADE)
    # owner = models.ForeignKey(User) і payment_account
    apartment_number = models.CharField(max_length=10)
    area = models.FloatField()
