from django.db import models
from django.conf import settings


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=120) # 영화 제목
    poster_url = models.ImageField(blank=True) # 영화 포스터
    audiCnt = models.IntegerField() # 해당일 관객수
    audinten = models.IntegerField() # 전일 대비 증감수
    audiChange = models.FloatField() # 전일 대비 증감 비율
    auidAcc = models.IntegerField() # 누적 관객수
    userRating = models.FloatField() # 영화 평점
    
class Match(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # up = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="up", blank=True,null=True)
    # down = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,null=True)
    user_up = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="up",blank=True)
    user_down = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="down",blank=True)
    standard = models.PositiveIntegerField(default = 0)
    date = models.DateField(auto_now_add=True)