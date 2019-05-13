from django.shortcuts import render
import datetime
import requests
import json
from .models import Movie
import os

# Create your views here.
naver_secret = os.getenv('NAVERSECRET')
naver_id = os.getenv("NAVERID")


def test(request):
    return render(request, 'index.html')
    
    
def getmoviedatalocal():

    today = datetime.datetime.today()
    # print(int(today.strftime("%Y%m%d"))-1)
    today = int(today.strftime("%Y%m%d"))-1
    # print("오늘입니다")
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?"
    params={
      'key':'db2280283c7ae6f2389c5ab040847efe',
      'targetDt':today,
    #   'itemPerPage':'10',
    }
    
    headers = {
        'X-Naver-Client-Id': naver_id,
        'X-Naver-Client-Secret': naver_secret
    }
    res = requests.get(url,params=params).text
    doc = json.loads(res)
    # print(doc['boxOfficeResult']['dailyBoxOfficeList'][0])
    # length = len(doc['boxOfficeResult']['dailyBoxOfficeList'])
    for a in range(10):
        title = doc['boxOfficeResult']['dailyBoxOfficeList'][a]['movieNm']
        audiCnt = doc['boxOfficeResult']['dailyBoxOfficeList'][a]['audiCnt']
        audinten = doc['boxOfficeResult']['dailyBoxOfficeList'][a]['audiInten']
        audiChange = doc['boxOfficeResult']['dailyBoxOfficeList'][a]['audiChange']
        auidAcc = doc['boxOfficeResult']['dailyBoxOfficeList'][a]['audiAcc']
        
        naver_url = "https://openapi.naver.com/v1/search/movie?query="+title
        
        response = requests.get(naver_url, headers=headers).text
        document = json.loads(response)['items'][0]
        print(document)
        
        
        userRating = document['userRating']
        poster_url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='+document['link'].split('=')[1]
        
        movie = Movie()
        movie.title = title
        movie.poster_url = poster_url
        movie.audiCnt = audiCnt
        movie.audinten = audinten
        movie.audiChange = audiChange
        movie.auidAcc = auidAcc
        movie.userRating = userRating
        movie.save()
    
    
# 아래 실행하면 영진위에서 영화 정보 받은 다음에 DB에 저장
getmoviedatalocal()

def movieList(request):
    movie = Movie.objects.all()
    print(movie)
    return render(request, 'index.html', {'movies':movie})


# class Movie(models.Model):
#     title = models.CharField(max_length=120) # 영화 제목
#     poster_url = models.ImageField(blank=False) # 영화 포스터
#     audiCnt = models.IntegerField() # 해당일 관객수
#     audinten = models.IntegerField() # 전일 대비 증감수
#     audiChange = models.IntegerField() # 전일 대비 증감 비율
#     auidAcc = models.IntegerField() # 누적 관객수
#     userRating = models.IntegerField() # 영화 평점