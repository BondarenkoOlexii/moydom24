from django.db import models
from src.common.models import SeoBlock, Image
from src.adminpanel.models.SiteChoise import PageChoise
# Create your models here.

class Main_Page(models.Model):
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)
    name = models.CharField(20)
    description = models.TextField()
    image_1 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='main_image_1')
    image_2 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='main_image_2')
    image_3 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='main_image_3')
    type = models.CharField(
        max_length=10,
        choices=PageChoise.choices,
        default=PageChoise.main,
    )


class About_Page(models.Model):
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)
    name = models.CharField(20)
    description = models.TextField()
    document = models.FileField()
    manager_photo = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='image_manager')
    image_1 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='about_image_1')
    image_2 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='about_image_2')
    image_3 = models.OneToOneField(Image, on_delete=models.CASCADE, related_name='about_image_3')


class Contact_Page(models.Model):
    seoblock = models.OneToOneField(SeoBlock, on_delete=models.SET_NULL, null=True)
    name = models.CharField(20)
    description = models.TextField()
    url = models.URLField()
    coordinate = models.TextField()
    full_name = models.CharField(max_length=220)
    location = models.TextField()
    adress = models.TextField()
    email_adress = models.EmailField()




class Additional_Block(models.Model):
    main_page = models.ForeignKey(Main_Page, on_delete=models.CASCADE, null=True, blank=True)
    about_page = models.ForeignKey(About_Page, on_delete=models.CASCADE, null=True, blank=True)

    additional_name = models.CharField(max_length=20)
    additional_description = models.TextField()
    additional_image = models.OneToOneField(Image, on_delete=models.CASCADE)