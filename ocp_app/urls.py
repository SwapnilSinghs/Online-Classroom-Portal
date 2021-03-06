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
    path('signOut/', views.signOut, name='signOut'),
    path('announcements/', views.announcements, name='announcements'),
    path('add_announcement/', views.add_announcement, name='add_announcement'),
    path('addAnnouncements/', views.addAnnouncements, name='addAnnouncements'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path('forum/', views.forum, name='forum'),
    path('add_course/', views.add_course, name='add_course'),
    path('del_course/', views.del_course, name='del_course'),
    path('home/', views.home, name='home'),
    #path('dashboardTeach/', views.dashboardTeach, name='dashboardTeach'),
    path('homeTeach/', views.homeTeach, name='homeTeach'),
    path('view_material/<str:cid>',views.view_material,name='view_material'),
    path('addMaterial/<str:cid>',views.addMaterial,name='addMaterial'),
    path('add_Material/<str:cid>',views.add_Material,name='add_Material'),
    path('viewStudent/',views.viewStudent,name='viewStudent'),
    path('search_student/',views.search_student,name='search_student'),
    path('viewQuery/',views.view_query,name='viewQuery'),
]
