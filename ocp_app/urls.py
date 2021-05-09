from django.urls import path
from . import views

urlpatterns = [
    path('signUpStud/', views.signUpStud, name='signUpStud'),
    path('signIn/', views.signIn, name='signIn'),
    path('signUpTeach/', views.signUpTeach, name='signUpTeach'),
    path('mainPage/', views.mainPage, name='mainPage'),
    path('verifyOTP/', views.verifyOTP, name='verifyOTP'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courseStud/', views.courseStud, name='courseStud'),
    path('addCourse/', views.addCourse, name='addCourse'),
    path('signOut/',views.signOut,name='signOut'),
    path('announcements/',views.announcements,name='announcements'),
    path('new_announcements/',views.newannouncements,name='new_announcements'),
    path('addAnnouncements/',views.addAnnouncements,name='addAnnouncements'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
]
