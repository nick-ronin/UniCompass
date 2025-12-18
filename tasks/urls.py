# урлы для задач
from django.urls import path
from . import views

urlpatterns = [
    path('tasklist/', views.tasklist_page, name='tasklist'),
    path('all_tasks/', views.all_tasks_admin, name='all_tasks'),
    path('assign_task/', views.assign_task, name='assign_task'),
    ]
