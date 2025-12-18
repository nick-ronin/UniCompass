from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from django.utils import timezone

class Task(models.Model):
    id_gen_tasks = models.AutoField(primary_key=True)
    title = models.TextField(max_length=50, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание задачи')
    type = models.TextField(verbose_name='Тип задачи')
    deadline = models.DateField(verbose_name='Дедлайн задачи')
    assign_to = models.TextField(verbose_name='Кому предназначена задача')
    # priority = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ('low', 'Низкий'),
    #         ('medium', 'Средний'),
    #         ('high', 'Высокий')], 
    #     verbose_name='Приоритет')
    class Meta:
        db_table = 'general_tasks'
    
class StudentGeneralTask(models.Model):

    STATUS_CHOICES = (
        ("not_done", "Не выполнено"),
        ("in_progress", "В процессе"),
        ("done", "Выполнено"),
    )

    id_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column='id_user')
    id_gen_task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT,
        db_column='id_gen_task')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="not_done"
    )
    deadline = models.DateField(verbose_name='Дедлайн задачи', null=True, blank=True, default=timezone.now)

    class Meta:
        db_table = 'students_general_tasks'
        unique_together = ("id_user", "id_gen_task")