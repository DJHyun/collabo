from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import get_user_model
from .forms import UserCustomCreationForm

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
    
def user_detail(request,user_id):
    user_infos = get_user_model().objects.get(id=user_id)
    if request.user.is_authenticated:
        recommend_movie = Score.objects.filter(user__in=request.user.followings.values('id')).order_by('-value').first()
    else:
        recommend_movie = Score.objects.order_by('-value').first()
    context={
        'user_infos':user_infos,
        'recommend_movie':recommend_movie,
    }
    return render(request,'accounts/userdetail.html',context)


def up_money(request,user_id,movie_id):
    pass


def down_money(request,user_id,movie_id):
    pass