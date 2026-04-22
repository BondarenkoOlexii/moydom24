from django.db import models

from src.adminpanel.models.FinanceChoise import TransactionChoise, InvoiceChoise
from src.finance.models import Payment_Account, Cash_Register
from src.adminpanel.models.SettingChoise import CountersChoise
from src.adminpanel.models.FinanceChoise import CashRegisterChoise


# Create your models here.

class Tariff(models.Model):
    name = models.CharField(max_length=220)
    description = models.TextField()
    create_time = models.DateTimeField(auto_now=True, null=True, blank=True)

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
    account = models.ForeignKey(Payment_Account, on_delete=models.CASCADE)
    indicator = models.CharField(max_length=20)
    status = models.CharField(choices=CountersChoise.choices, default=CountersChoise.choices[0][0])



class Transaction(models.Model):
    cash_register = models.ForeignKey(Cash_Register, on_delete=models.CASCADE)
    status = models.CharField(TransactionChoise.choices, default=TransactionChoise.choices[0][0])
    amount = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    service = models.ManyToManyField(Service)


class Invoice(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    total_amount = models.CharField(max_length=10)
    type = models.CharField(choices=InvoiceChoise.choices, default=InvoiceChoise.choices[0][0])
    comment = models.TextField()
    create_time = models.DateTimeField()


class PaymentInfo(models.Model):
    name = models.CharField()
    information = models.TextField()


class TransactionPurpose(models.Model):
    name = models.CharField(max_length=225)
    type = models.CharField(choices=CashRegisterChoise, default=CashRegisterChoise.choices[0][0])

