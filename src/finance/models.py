from django.db import models
from src.houses.models import Apartment
from src.adminpanel.models.FinanceChoise import CashRegisterChoise
from src.adminpanel.models.UserChoise import AccountStatus
from src.settings.models import Service, Tariff, Measurement
from src.adminpanel.models.FinanceChoise import TransactionChoise
from src.adminpanel.models.FinanceChoise import InvoiceChoise
# Create your models here.

class Payment_Account(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    bank_book = models.CharField(max_length=220, unique=True)
    balance = models.CharField(max_length=10, default=0)
    create_time = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=AccountStatus)


class Cash_Register(models.Model):
    account = models.OneToOneField(Payment_Account, on_delete=models.CASCADE)
    create_time = models.DateTimeField()
    type = models.CharField(choices=CashRegisterChoise.choices)
    sum = models.CharField(max_length=10)


class Transaction(models.Model):
    cash_register = models.ForeignKey(Cash_Register, on_delete=models.CASCADE)
    status = models.CharField(TransactionChoise.choices, default=TransactionChoise.choices[0][0])
    amount = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    service = models.ManyToManyField(Service)


class Invoice(models.Model):
    invoice_unique_id = models.IntegerField(unique=True)
    service = models.ManyToManyField(Service, through='ThoughInvoiceService')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True, blank=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.CharField(max_length=10, null=True, blank=True)
    type = models.CharField(choices=InvoiceChoise.choices, default=InvoiceChoise.choices[0][0])
    status = models.BooleanField(default=True)
    payment_account = models.OneToOneField(Payment_Account, on_delete=models.CASCADE)
    create_time = models.DateField()
    period_start = models.DateField()
    period_end = models.DateField()



class ThoughInvoiceService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    indicator = models.CharField(max_length=20)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, null=True, blank=True)
    measurement_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)