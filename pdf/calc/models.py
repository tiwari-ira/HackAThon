from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class PDFU(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)

class USE(models.Model):
    username = models.CharField(max_length=30)
    operation = models.CharField(max_length=20)
    created = models.DateTimeField()
    ip_address = models.GenericIPAddressField()

