# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'), 
    path('profile/', views.profile_page, name='profile'),
    path('student_detail/<int:id_user>/', views.student_detail_admin, name='student_detail'),
    path('all_students/', views.admin_all_students_page, name='all_students'),
    ]
