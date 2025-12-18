from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):

    id_user = models.AutoField(primary_key=True)  
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)  
    role = models.CharField(
        max_length=50, 
        choices=[
            ('student', 'Студент'),
            ('admin', 'Администратор'),
        ], verbose_name='Роль')
    passport_number = models.CharField(max_length=20, unique=True)
    citizenship = models.CharField(max_length=100)
    institute = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'surname']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.email
    
    # Методы для Django admin
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin











# from django.db import models

# class User(models.Model):
#     id_user = models.AutoField(primary_key=True)  
#     first_name = models.CharField(max_length=100, verbose_name='Имя')
#     surname = models.CharField(max_length=100, verbose_name='Фамилия')
#     patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
#     address = models.TextField(verbose_name='Адрес')  
#     phone_number = models.CharField(max_length=20, verbose_name='Телефон')
#     email = models.EmailField(unique=True, verbose_name='Email')
#     role = models.CharField(
#         max_length=50, 
#         choices=[
#             ('student', 'Студент'),
#             ('admin', 'Администратор'),
#         ], verbose_name='Роль')
#     passport_number = models.CharField(max_length=20, unique=True, verbose_name='Номер паспорта')
#     citizenship = models.CharField(max_length=100, verbose_name='Гражданство')
#     institute = models.CharField(max_length=100, verbose_name='Институт')
#     group = models.CharField(max_length=100, verbose_name='Группа')
#     course = models.CharField(max_length=100, verbose_name='Курс')
#     class Meta:
#             db_table = 'users'  

