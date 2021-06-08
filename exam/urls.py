from django.urls import path
from . import views

urlpatterns = [
    path('examDashboard/',views.examDashboard,name='examDashboard'),
    path('addAssignment/',views.addAssignment,name='addAssignment'),
    path('viewAssignment/',views.viewAssignment,name='viewAssignment'),
    path('addExam/',views.addExam,name='addExam'),
]