from django.db import models


class PageChoise(models.TextChoices):
    main = 'main', 'main'
    service = 'service', 'service'