from django.shortcuts import render,redirect
import datetime
import requests
import json
from .models import Movie,Match,UserMatchMoney
import os
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required

# Create your views here.
naver_secret = os.getenv('NAVERSECRET')
naver_id = os.getenv("NAVERID")


def test(request):
    return render(request, 'index.html')
    
    
def getmoviedatalocal(request):#데이터수집 영진위에서는 관객정보를 , 네이버에서는 이미지를 긁어옴
    if request.user.is_superuser:
        today1 = datetime.datetime.today()
        # print(today1.strftime("%Y-%m-%d"))
        # print(int(today.strftime("%Y%m%d"))-1)
        today = int(today1.strftime("%Y%m%d"))-1
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?"
        params={
          'key':'db2280283c7ae6f2389c5ab040847efe',
          'targetDt':today,
        #   'itemPerPage':'10',
        }
        #네이버는 환경변수로 저장함
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
            userRating = document['userRating']
            img_url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='+document['link'].split('=')[1]
            
            response2 = requests.get(img_url).text
            soup = BeautifulSoup(response2,'html.parser')
            all_divs = soup.find("img")
            poster_url = all_divs.get('src')
            
            movie = Movie()
            movie.title = title
            movie.poster_url = poster_url
            movie.audiCnt = audiCnt
            movie.audinten = audinten
            movie.audiChange = audiChange
            movie.auidAcc = auidAcc
            movie.userRating = userRating
            movie.date = today1.strftime("%Y-%m-%d")
            movie.save()
            
            match = Match(movie=movie,standard=movie.audiCnt)
            match.save()
    return redirect("movies:list")

def movieList(request):
    today1 = datetime.datetime.today()
    # today = int(today.strftime("%Y%m%d"))-1#어제꺼를 기준으로 해야하므로
    print(today1.strftime("%Y-%m-%d"))
    # print(today1.strftime("%Y-%m-(%d-1)"))
    # movies = Movie.objects.filter(date=today1.strftime("%Y-%m-%d"))
    # movies = Movie.objects.all()
    
    matches = Match.objects.filter(date=today1.strftime("%Y-%m-%d"))
    
    return render(request, 'index.html', {'matches':matches})

def moviedetail(request,movie_id):
    movie = Movie.objects.get(pk=movie_id)
    
    return render(request,'detail.html',{'movie':movie})

#모모 구매
@login_required
def predict(request):
    today1 = datetime.datetime.today()
    matches = Match.objects.filter(date=today1.strftime("%Y-%m-%d"))
    return render(request,'predict.html',{'matches':matches})
        
        
# 아래 실행하면 영진위에서 영화 정보 받은 다음에 DB에 저장
# getmoviedatalocal()
# print('다운 끝')