from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('signUpStud/', views.signUpStud, name='signUpStud'),
]