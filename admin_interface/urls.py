from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.home, name='login'),
    path('signinhandle/',views.signinhandle,name='signinhandle'),
    path('signup/',views.signup,name='signup'),
    path('signuphandle/',views.signuphandle,name='signuphandle'),
    path('dashboard/',views.admin_dashboard,name='dashboard'),
    path('signOut/',views.signOut,name='signOut'),
   
   
   
]