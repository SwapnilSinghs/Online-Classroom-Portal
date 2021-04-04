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
]
