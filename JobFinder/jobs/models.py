from django.db import models

# Create your models here.
class Offer(models.Model):
    name = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    publication_date = models.CharField(max_length=40)
    city = models.CharField(max_length=25, null=True)