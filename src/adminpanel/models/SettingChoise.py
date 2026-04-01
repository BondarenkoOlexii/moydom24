from django.db import models

class CountersChoise(models.TextChoices):
    new = 'new', 'Нове'
    considered = 'considered', 'Враховане'
    no_considered = 'no_considered', 'Не враховане'