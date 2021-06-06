from django.urls import path
from . import views

urlpatterns = [
    path('examDashboard/',views.examDashboard,name='examDashboard'),
    path('addAssignment/',views.addAssignment,name='addAssignment'),
    path('addExam/',views.addExam,name='addExam'),
]