from django.db import models

from src.adminpanel.models.SettingChoise import CountersChoise
from src.adminpanel.models.FinanceChoise import CashRegisterChoise
from src.houses.models import Apartment


# Create your models here.

class Tariff(models.Model):
    name = models.CharField(max_length=220)
    description = models.TextField()
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    unit_of_measurement = models.CharField(max_length=10)

    def __str__(self):
        return self.unit_of_measurement

class Service(models.Model):
    service = models.CharField(max_length=220)
    show = models.BooleanField(default=True)
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, blank=True, null=True)
    tariff = models.ManyToManyField(Tariff)

    def __str__(self):
        return self.service

class Tarrif_Service_Price(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)



class Counters(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    indicator = models.CharField(max_length=20)
    special_id = models.CharField(max_length=220, unique=True)
    status = models.CharField(choices=CountersChoise.choices, default=CountersChoise.choices[0][0])
    create_time = models.DateField()


class PaymentInfo(models.Model):
    name = models.CharField()
    information = models.TextField()


class TransactionPurpose(models.Model):
    name = models.CharField(max_length=225)
    type = models.CharField(choices=CashRegisterChoise, default=CashRegisterChoise.choices[0][0])

