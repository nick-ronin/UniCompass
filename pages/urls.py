from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('tasks/', views.tasks, name='tasks'),
    path('knowledge-base/', views.knowledge_base, name='knowledge_base'),
    path('contacts/', views.contacts, name='contacts'),
    path('set-language/', views.set_language, name='set_language'),
    path('mfc/', views.mfc_detail, name='mfc_detail'),
]

