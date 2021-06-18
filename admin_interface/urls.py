from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.home, name='login'),
    path('signinhandle/',views.signinhandle,name='signinhandle'),
    path('signup/',views.signup,name='signup'),
    path('signuphandle/',views.signuphandle,name='signuphandle'),
    path('dashboard/',views.admin_dashboard,name='dashboard'),
    path('signOut/',views.signOut,name='signOut'),
    path('viewAnnouncement/',views.viewAnnouncements,name='viewAnnouncement'),
    path('addAnnouncement/',views.addAnnouncements,name='addAnnouncement'),
    path('add_announcement/',views.add_announcement,name='add_announcement'),
    path('del_announce/',views.del_announce,name='del_announce'),
    path('createDepartment/',views.createDepartment,name='createDepartment'),
    path('create_Department/',views.create_Department,name='create_Department'),
    path('viewDepartment/',views.viewDepartment,name='viewDepartment'),
    path('del_department/',views.del_department,name='del_department'),
    path('viewStudent/',views.viewStudent,name='viewStudent'),
    path('search_student/',views.search_student,name='search_student'),
    path('viewStudent/',views.viewStudent,name='viewStudent'),
    path('search_student/',views.search_student,name='search_student'),
    path('viewFaculty/',views.viewFaculty,name='viewFaculty'),
    path('search_faculty/',views.search_student,name='search_faculty'),
    path('del_student/',views.del_student,name='del_student'),
    path('del_teacher/',views.del_teacher,name='del_teacher'),
]

   
   
