from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import get_user_model
from .forms import UserCustomCreationForm
from momo.models import Movie, Match, UserMatchMoney

# Create your views here.



@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
        
    if request.method == 'POST':
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('movies:list')
    else:
        user_form = UserCustomCreationForm()
        
    context = {'form': user_form}
    return render(request, 'accounts/forms.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('movies:list')
    else:
        login_form = AuthenticationForm()
    context = {'form': login_form}
    return render(request, 'accounts/forms.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:list')
    
def user_info(request):
    users = get_user_model().objects.all()
    context={
        'users':users,
    }
    return render(request,'accounts/userlist.html',context)

@login_required
def user_detail(request,user_id):
    user_infos = get_user_model().objects.get(pk=user_id)
    matches = UserMatchMoney.objects.filter(user=user_id)
    # if request.user.is_authenticated:
    #     recommend_movie = Score.objects.filter(user__in=request.user.followings.values('id')).order_by('-value').first()
    # else:
    #     recommend_movie = Score.objects.order_by('-value').first()
    context={
        'user_infos':user_infos,
        # 'recommend_movie':recommend_movie,
        'matches':matches
    }
    return render(request,'accounts/userdetail.html',context)




def up_money(request,match_id):
    print("여기 안들어옴?")
    match = get_object_or_404(Match,pk=match_id)
    usermatchmoney = UserMatchMoney(match=match_id,user=request.user)
    usermatchmoney.updown = 1 #up은 1
    usermatchmoney.points = request.points
    request.user.points -= request.points
    if request.user in match.user_down.all():
        match.user_down.remove(request.user)
        
    if request.user in match.user_up.all():
        match.user_up.remove(request.user)
    else:
        match.user_up.add(request.user)

    return redirect("movies:list")


def down_money(request,match_id):

    match = get_object_or_404(Match,pk=match_id)
    usermatchmoney = UserMatchMoney(match=match_id,user=request.user)
    usermatchmoney.updown = 2 #down은 2
    usermatchmoney.points = request.points
    request.user.points -= request.points
    if request.user in match.user_up.all():
        match.user_up.remove(request.user)
    if request.user in match.user_down.all():
        match.user_down.remove(request.user)
    else:
        match.user_down.add(request.user)
    
    #여기 바꿔야됨
    return redirect("movies:list")

@login_required    
def purchase(request,match_id):
    points = int(request.POST["points"])
    
    if request.user.points>=points:
        if request.POST["updown_code"]=='1':
            match = get_object_or_404(Match,pk=match_id)
            usermatchmoney = UserMatchMoney(match=match,user=request.user)
            usermatchmoney.updown = 1 #up은 1
            usermatchmoney.points = points
            usermatchmoney.save()
            request.user.points -= points
            request.user.save()
            if request.user in match.user_down.all():
                match.user_down.remove(request.user)
                
            if request.user in match.user_up.all():
                match.user_up.remove(request.user)
            else:
                match.user_up.add(request.user)
        
            return redirect("movies:predict")
            
        elif request.POST["updown_code"]=='2':
            match = get_object_or_404(Match,pk=match_id)
            usermatchmoney = UserMatchMoney(match=match,user=request.user)
            usermatchmoney.updown = 2 #down은 2
            usermatchmoney.points = points
            usermatchmoney.save()
            request.user.points -= points
            request.user.save()
            if request.user in match.user_up.all():
                match.user_up.remove(request.user)
            if request.user in match.user_down.all():
                match.user_down.remove(request.user)
            else:
                match.user_down.add(request.user)
            
            #여기 바꿔야됨
            return redirect("movies:predict")
            
        # return redirect("movies:list")
    else:
        #여긴 돈 부족할때
        return redirect("movies:predict")

@login_required
def refund(request,match_id):
    usermatchmoney = get_object_or_404(UserMatchMoney,match=match_id,user=request.user)
    usermatchmoney.delete()
    return redirect('movies:list')
    
    
    