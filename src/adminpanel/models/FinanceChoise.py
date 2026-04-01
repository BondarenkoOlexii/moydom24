from django.db import models


class CashRegisterChoise(models.TextChoices):
    arrival = 'arrival ', 'Приход'
    expense = 'expense', 'Расход'

class TransactionChoise(models.TextChoices):
    no_conducted = 'no_conducted', 'Не проведена'
    conducted = 'conducted', 'Проведена'

class InvoiceChoise(models.TextChoices):
    no_paid = 'no_paid', 'Не оплачено'
    partially = 'partially', 'Частично'
    paid = 'paid', 'Оплачено'