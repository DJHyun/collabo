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
    date = models.DateField()
    
    def __str__(self):
        return self.title
        
class Match(models.Model):
    
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_up = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="up",blank=True)
    user_down = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="down",blank=True)
    standard = models.PositiveIntegerField(default = 0)# 기준관객수
    date = models.DateField(auto_now_add=True)# 날짜
    uprate = models.FloatField(default = 1)#up 배당
    downrate = models.FloatField(default = 1)#down 배당
    
    def __str__(self):
        return f'{self.movie} + {self.date}'
        
class UserMatchMoney(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    updown = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    win = models.IntegerField(default=0)#0은 아직 상태 모름 1은 이김 2는 짐