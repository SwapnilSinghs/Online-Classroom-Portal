from django.db import models
from ocp_app.models import Courses,Student,Teacher

# Create your models here.
class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length = 255,default="")
    exam_type = models.CharField(max_length = 255,default="")
    exam_date = models.DateField(blank=True, null=True)
    exam_start_time = models.TimeField(blank=True, null=True)
    exam_end_time = models.TimeField(blank=True, null=True)
    exam_detail = models.CharField(max_length = 255,default="") 
    exam_fileUpload = models.FileField(upload_to='uploads/')
    course = models.ForeignKey(Courses, to_field='course_id', on_delete=models.CASCADE,null=True)
    dept = models.CharField(max_length=255,default="")
    uploaded_by = models.ForeignKey(Teacher, to_field='username', on_delete=models.CASCADE,null=True)
    exam_marksOutOf = models.DecimalField(max_digits = 6,decimal_places = 2,default=0)

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length = 255)
    assignment_date = models.DateField(blank=True, null=True)
    assignment_start_time = models.TimeField(blank=True, null=True)
    assignment_end_time = models.TimeField(blank=True, null=True)
    assignment_detail = models.CharField(max_length = 255,default="") 
    assignment_fileUpload = models.FileField(upload_to='uploads/')
    course = models.ForeignKey(Courses, to_field='course_id', on_delete=models.CASCADE,null=True)
    dept = models.CharField(max_length=255,default="")
    uploaded_by = models.ForeignKey(Teacher, to_field='username', on_delete=models.CASCADE,null=True)
    assignment_marksOutOf = models.DecimalField(max_digits = 6,decimal_places = 2,default=0)

class AssignmentAnswer(models.Model):
    sno = models.AutoField(primary_key=True)
    assign = models.ForeignKey(Assignment, to_field='assignment_id', on_delete=models.CASCADE,null=True)
    stud = models.ForeignKey(Student, to_field='username', on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Courses, to_field='course_id', on_delete=models.CASCADE,null=True)
    submittedfile = models.FileField(upload_to='uploads/')
    date = models.DateTimeField(auto_now=True)
    amarksObtained = models.DecimalField(max_digits = 6,decimal_places = 2,default=0)
    amarksOutOf = models.DecimalField(max_digits = 6,decimal_places = 2,default=0)

class ExamAnswer(models.Model):
    sno = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, to_field='exam_id', on_delete=models.CASCADE,null=True)
    stud = models.ForeignKey(Student, to_field='username', on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Courses, to_field='course_id', on_delete=models.CASCADE,null=True)
    submittedfile = models.FileField(upload_to='uploads/')
    date = models.DateTimeField(auto_now=True)
    emarksObtained = models.DecimalField(max_digits = 6,decimal_places = 2,default=0)
    emarksOutOf = models.DecimalField(max_digits = 6,decimal_places = 2,default=0)

# class Result(models.Model):
#     result_id = models.AutoField(primary_key=True)
#     stud_id = models.ForeignKey(Student, to_field='username', on_delete=models.CASCADE,null=True)
#     course = models.ForeignKey(Courses, to_field='course_id', on_delete=models.CASCADE,null=True)
#     dept = models.CharField(max_length=255,default="")
#     exam_type = models.CharField(max_length = 255,default="")
#     total_marks = models.DecimalField(max_digits = 6,decimal_places = 2)
#     obtained_marks = models.DecimalField(max_digits = 6,decimal_places = 2)

class Query(models.Model):
    query_id = models.AutoField(primary_key=True)
    stud_id = models.ForeignKey(Student, to_field='username', on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Courses, to_field='course_id', on_delete=models.CASCADE,null=True)
    exam_type = models.CharField(max_length = 255,default="")
    query_subject = models.CharField(max_length=255,default="")
    msg = models.CharField(max_length=255,default="")
    datetime = models.DateTimeField(auto_now=True)  
