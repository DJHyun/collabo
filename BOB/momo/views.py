from django.shortcuts import render,redirect,get_object_or_404
import datetime
import requests
import json
from .models import Movie,Match,UserMatchMoney,Score
from .forms import ScoreForm
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
        for i in range(3,0,-1):
            today = int(today1.strftime("%Y%m%d"))-i
            today2 = today1.strftime("%Y-%m-")
            yesterday = today2+str(today1.day-i+1)
            # print(today1.strftime("%Y-%m-%d"))
            # print(int(today.strftime("%Y%m%d"))-1)
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
                # movie.date = today1.strftime("%Y-%m-%d")
                movie.date = yesterday
                movie.save()
                
                match = Match(movie=movie,standard=movie.audiCnt,date=yesterday)
                audiChange = float(audiChange)
                if audiChange<0:
                    if 0.7*abs(audiChange)>1000:
                        audiChange/=1000
                    elif 0.7*abs(audiChange)>100:
                        audiChange/=100
                    elif 0.7*abs(audiChange)>10:
                        audiChange/=10
                    elif 0.7*abs(audiChange)>5:
                        audiChange/=5
                    elif 0.7*abs(audiChange)>2:
                        audiChange/=2
                    downrate = 1+0.7*abs(audiChange)
                    uprate = 4/downrate
                    if uprate<1:
                        uprate+=1
                    if downrate>5:
                        downrate/=2
                else:
                    if 0.7*abs(audiChange)>1000:
                        audiChange/=1000
                    elif 0.7*abs(audiChange)>100:
                        audiChange/=100
                    elif 0.7*abs(audiChange)>10:
                        audiChange/=10
                    elif 0.7*abs(audiChange)>5:
                        audiChange/=5
                    elif 0.7*abs(audiChange)>2:
                        audiChange/=2
                    uprate = 1+0.7*abs(audiChange)
                    downrate = 4/uprate
                    if downrate<1:
                        downrate+=1
                    if uprate>5:
                        uprate/=2
                match.uprate = uprate
                match.downrate = downrate
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
    score_form = ScoreForm()
    return render(request, 'index.html', {'matches':matches,'score_form':score_form})

def moviedetail(request,movie_id):
    movie = Movie.objects.get(pk=movie_id)
    
    return render(request,'detail.html',{'movie':movie})

#모모 구매
@login_required
def predict(request):
    today1 = datetime.datetime.today()
    matches = Match.objects.filter(date=today1.strftime("%Y-%m-%d"))
    return render(request,'predict.html',{'matches':matches})

# 지난 momo 정보
def history(request):
    momos = Match.objects.exclude(date=datetime.datetime.today()).order_by('-date')
    return render(request,'history.html',{'momos':momos})
        
# 아래 실행하면 영진위에서 영화 정보 받은 다음에 DB에 저장
# getmoviedatalocal()
# print('다운 끝')


# def momodetail(request,match_id):
#     return


@login_required
def create_score(request,match_id):
    score_form = ScoreForm(request.POST)
    if score_form.is_valid():
        score = score_form.save(commit=False)
        score.user = request.user
        score.match_id = match_id
        score.save()
        
    return redirect('movies:list')

def score_delete(request,match_id,score_id):
    score = get_object_or_404(Score,pk=score_id)
    if score.user==request.user:
        score.delete()
    return redirect('movies:list')
    
    
    
    # 참고해보자..
# https://github.com/anhaeh/forms-vue.js-django/blob/master/app/views.py


# @api_view(['POST'])
# def create_score(request, match_id):
#     match = get_object_or_404(Match,pk=match_id)
#     serializer = ScoreSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#         return Response({"messages":"작성되었습니다."})
        
# @api_view(['GET','PUT','DELETE'])        
# def score(request,score_pk):
#     score = get_object_or_404(Score, pk=score_pk)
#     if request.method =="GET":# 보여주기
#         serializer = ScoreSerializer(score,many=False)
#         return Response(data=serializer.data)
        
#     elif request.method =="PUT":# 업데이트
#         serializer = ScoreSerializer(score,many=False,data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({"messages":"수정되었습니다."})
        
#     elif request.method =="DELETE":
#         score.delete()
#         return Response({"message":"삭제되었습니다!"})

def recommandmovie(request):

    recommand_movie = Match.objects.order_by('-usercnt').first()
    
    context = {
        'recommandmovie':recommand_movie,
    }
    return render(request,"recommand.html",context)