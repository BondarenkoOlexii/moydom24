from django.db import models

class Language(models.TextChoices):
    ru = 'ru', 'ru'
    uk = 'uk', 'uk'
    eng = 'eng', 'eng'

class Role(models.TextChoices):
    director = 'director', 'Директор'
    manager = 'manager', 'Менеджер'
    electrician = 'electrician', 'Електрик'
    plumber = 'plumber', 'Сантехник'

class Status(models.TextChoices):
    new = 'new', 'Нове'
    in_progress = 'in_progress', 'В роботі'
    completed = 'completed', 'Виконано'

class UserStatus(models.TextChoices):
    active = 'active', 'Активен'
    new = 'new', 'Новий'
    inactive = 'inactive', 'Отключен'