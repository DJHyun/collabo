from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    points = models.PositiveIntegerField(default=0)
    bank = models.CharField(blank=False, max_length=120)
    
class Money(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    money = models.PositiveIntegerField(blank=False)
    status = models.TextField()
    date = models.DateField() 
    check_date = models.DateField(null=True)
    
    def __str__(self):
        return f'{self.user} 님이 {self.money} MoMo 환전 신청 하였습니다.'