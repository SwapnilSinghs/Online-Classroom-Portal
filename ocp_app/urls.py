from django.urls import path
from . import views

urlpatterns = [
    path('signUpStud/', views.signUpStud, name='signUpStud'),
]