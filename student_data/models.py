from django.db import models
from users.models import User

class Insurance(models.Model):
    id_application = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        db_column='id_user')
    insurance_fee = models.CharField(max_length=100)
    application_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'На рассмотрении'),
            ('approved', 'Одобрено'),
            ('rejected', 'Отклонено'),
            ('active', 'Активно'),
        ]
    )
    insurance_company = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=100)

    class Meta:
        db_table = 'insurance'

# 
# 
# 
# 
# 
# таблица с поездками
# id_trip делается автоматом
class Trip(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,  # защита от удаления
        db_column='id_user' 
    )
    arrival_date = models.DateField()
    departure_date = models.DateField()
    
