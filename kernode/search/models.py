from django.db import models

# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    data = models.ImageField

class Video(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    data = models.FileField