from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Department(models.Model):
    snum = models.AutoField(primary_key=True)
    dept_id = models.CharField(max_length=3,default="",unique=True)
    dept_name = models.CharField(max_length=255,default="")

class Courses(models.Model):
    course_id = models.CharField(max_length = 150,primary_key=True,default=' ')
    course_name = models.CharField(max_length = 255,default=" ")
    dept = models.ForeignKey(Department,to_field='dept_id', on_delete=models.CASCADE) 
    year = models.CharField(max_length = 1,default="0")

class Student(models.Model):
    snum = models.AutoField(primary_key=True)
    img = models.ImageField(default="")
    username = models.CharField(max_length=15,default="")
    firstname = models.CharField(max_length=20,default="")
    lastname = models.CharField(max_length=20,default="")
    dob = models.DateField(blank=True, null=True)
    dept = models.CharField(max_length=255,default="")
    email = models.CharField(max_length=100,default="")
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)],default="",help_text = "Enter 10 digit phone number")
    password = models.CharField(max_length=20, default="")
    year = models.CharField(max_length = 1,default="0")    
    course = models.ForeignKey(Courses, to_field='course_id', on_delete=models.CASCADE,null=True)

class Teacher(models.Model):
    tnum = models.AutoField(primary_key=True)
    img = models.ImageField(default=" ")
    username = models.CharField(max_length=15,default="")
    firstname = models.CharField(max_length=20,default="")
    lastname = models.CharField(max_length=20,default="")
    dob = models.DateField(blank=True, null=True)
    dept = models.CharField(max_length=255,default="")
    email = models.CharField(max_length=100,default="")
    phone = models.CharField(max_length=10,validators=[MinLengthValidator(10)],default="",help_text = "Enter 10 digit phone number")
    designation = models.CharField(max_length = 15,default=" ")
    password = models.CharField(max_length=20, default="")
    course = models.ForeignKey(Courses, to_field='course_id', on_delete=models.CASCADE,null=True)

class studyMaterial(models.Model):
    material_id=models.IntegerField()
    material_type= models.CharField(max_length = 15)
    material_DESC = models.CharField(max_length = 15)
    material = models.FileField(upload_to='uploads/')
    department = models.ForeignKey(Department,to_field='dept_id', on_delete=models.CASCADE)
    course = models.ForeignKey(Courses,to_field='course_id', on_delete=models.CASCADE)
    
class Announcement(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    announcement_name = models.CharField(max_length = 50)
    department = models.ForeignKey(Department,to_field='dept_id', on_delete=models.CASCADE)
    detail = models.CharField(max_length = 150)
    announcement_file = models.FileField(upload_to='announcements/')
    date_of_announcement = models.DateField(blank=True, null=True)
    time_of_announcement = models.TimeField(auto_now=False, auto_now_add=False)