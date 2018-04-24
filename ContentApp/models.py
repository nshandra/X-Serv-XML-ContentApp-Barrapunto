from django.db import models

# Create your models here.
class Pages(models.Model):
    name = models.CharField(max_length=32)
    page = models.TextField()

class RSS(models.Model):
    link = models.TextField(unique=True)