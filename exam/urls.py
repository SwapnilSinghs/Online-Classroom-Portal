from django.urls import path
from . import views

urlpatterns = [
    path('examDashboard/',views.examDashboard,name='examDashboard'),
    path('addAssignment/',views.addAssignment,name='addAssignment'),
    path('viewAssignment/<int:assignid>',views.viewAssignment,name='viewAssignment'),
    path('viewExam/',views.viewExam,name='viewExam'),
    path('viewAllAssignment/',views.viewAllAssignment,name='viewAllAssignment'),
    path('viewAllExam/',views.viewAllExam,name='viewAllExam'),
    path('addExam/',views.addExam,name='addExam'),
]