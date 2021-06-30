from django.urls import path
from . import views

urlpatterns = [
    path('examDashboard/',views.examDashboard,name='examDashboard'),
    path('examlogin/',views.examlogin,name='examlogin'),
    path('examloginhandle/',views.examloginhandle,name='examloginhandle'),
    path('addAssignment/',views.addAssignment,name='addAssignment'),
    path('viewAssignment/<int:assignid>',views.viewAssignment,name='viewAssignment'),
    path('viewSubmitAssignTeach/<int:assignid>',views.viewSubmitAssignTeach,name='viewSubmitAssignTeach'),
    path('deleteAssignment/<int:assignid>',views.deleteAssignment,name='deleteAssignment'),
    path('viewExam/<int:examid>',views.viewExam,name='viewExam'),
    path('viewAllAssignment/',views.viewAllAssignment,name='viewAllAssignment'),
    path('submitAssignScore/<int:assignid>/<studid>',views.submitAssignScore,name='submitAssignScore'),
    path('viewAllExam/',views.viewAllExam,name='viewAllExam'),
    path('deleteExam/<int:examid>',views.deleteExam,name='deleteExam'),
    path('viewSubmitExamTeach/<int:examid>',views.viewSubmitExamTeach,name='viewSubmitExamTeach'),
    path('addExam/',views.addExam,name='addExam'),
    path('submitExamScore/<int:examid>/<studid>',views.submitExamScore,name='submitExamScore'),
]