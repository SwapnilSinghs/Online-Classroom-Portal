from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class SignUpStud(models.Model):
    snum = models.AutoField(primary_key=True)
    username = models.CharField(max_length=15,default="")
    firstname = models.CharField(max_length=20,default="")
    lastname = models.CharField(max_length=20,default="")
    email = models.CharField(max_length=100,default="")
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)],default="",help_text = "Enter 10 digit phone number")
    password = models.CharField(max_length=20, default="")

class Department(models.Model):
    snum = models.AutoField(primary_key=True)
    dept_id = models.CharField(max_length=3,default="")
    dept_name = models.CharField(max_length=255,default="")