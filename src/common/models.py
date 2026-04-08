from django.db import models

# Create your models here.

class SeoBlock(models.Model):
    title = models.CharField(max_length=20)
    keyword = models.CharField(max_length=20)
    description = models.TextField()

class Image(models.Model):
    photo = models.ImageField(upload_to='media')


# Якщо потрібно
# class ThourghtImage(models.Model):
#     image = models.ForeignKey(Image, on_delete=models.CASCADE)
#     image_type = models.CharField(max_length=125, choices=CommonType)
#
#     class Meta:
#         abstract = True