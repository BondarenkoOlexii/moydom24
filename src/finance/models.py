from django.db import models
from src.houses.models import Apartment
from src.adminpanel.models.FinanceChoise import CashRegisterChoise

# Create your models here.

class Payment_Account(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    bank_book = models.CharField(max_length=220, unique=True)
    balance = models.CharField(max_length=10)
    create_time = models.DateTimeField()

class Cash_Register(models.Model):
    account = models.OneToOneField(Payment_Account, on_delete=models.CASCADE)
    create_time = models.DateTimeField()
    type = models.CharField(choices=CashRegisterChoise.choices)
    sum = models.CharField(max_length=10)
