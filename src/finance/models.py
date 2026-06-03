from django.db import models
from src.houses.models import Apartment
from src.adminpanel.models.FinanceChoise import CashRegisterChoise
from src.adminpanel.models.UserChoise import AccountStatus
from src.settings.models import Service, Tariff, Measurement
from src.adminpanel.models.FinanceChoise import TransactionChoise
from src.adminpanel.models.FinanceChoise import InvoiceChoise
from src.users.models import User
# Create your models here.

class Payment_Account(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    bank_book = models.CharField(max_length=220, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=AccountStatus)

    def __str__(self):
        return f"{self.bank_book}"


class Cash_Register(models.Model):
    unique_id = models.CharField(unique=True)
    account = models.ForeignKey(Payment_Account, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_admin': True})
    create_time = models.DateField()
    type = models.CharField(choices=CashRegisterChoise.choices)
    status = models.BooleanField()
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(null=True, blank=True)
    article = models.CharField()


class Invoice(models.Model):
    invoice_unique_id = models.IntegerField(unique=True)
    service = models.ManyToManyField(Service, through='ThoughInvoiceService')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(choices=InvoiceChoise.choices, default=InvoiceChoise.choices[0][0])
    status = models.BooleanField(default=True)
    payment_account = models.ForeignKey(Payment_Account, on_delete=models.CASCADE)
    create_time = models.DateField()
    period_start = models.DateField()
    period_end = models.DateField()


class Transaction(models.Model):
    cash_register = models.ForeignKey(Cash_Register, on_delete=models.CASCADE, null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(TransactionChoise.choices, default=TransactionChoise.choices[0][0])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(auto_now=True)
    # service = models.ManyToManyField(Service)





class ThoughInvoiceService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    indicator = models.CharField(max_length=20)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, null=True, blank=True)
    measurement_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)