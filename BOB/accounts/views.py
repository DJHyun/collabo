from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import get_user_model
from .forms import UserCustomCreationForm,MoneyCreationForm
from momo.models import Movie, Match
from .models import Money

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
        
    context = {'form': user_form, 'flag':'one'}
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
    context = {'form': login_form, 'flag':'two'}
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
    user = get_user_model().objects.get(id=user_id)
    message = False
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            message = "수정되었습니다."
    form = UserCustomCreationForm(instance=user)
    context={
        'form':form,
        'message':message
    }
    return render(request, 'accounts/forms.html', context)
    
@login_required
def up_money(request,match_id):
    match = get_object_or_404(Match,pk=match_id)
    if request.user in match.user_up.all():
        match.user_up.remove(request.user)
    else:
        match.user_up.add(request.user)
    
    return redirect("movies:list")
    

@login_required
def down_money(request,match_id):
    match = get_object_or_404(Match,pk=match_id)
    if request.user in match.user_down.all():
        match.user_down.remove(request.user)
    else:
        match.user_down.add(request.user)
    
    return redirect("movies:list")
    
def money(request, flag, user_id):
    if request.method == 'POST':
        if flag == 1:
            pass
        elif flag == 2:
            user = get_object_or_404(get_user_model(), pk=user_id)
            user.points += int(request.POST['money'])
            user.save()
            return redirect("movies:list")
        else:
            user = get_object_or_404(get_user_model(), pk=user_id)
            Money.objects.create(user=user, money=int(request.POST['money']))
            return redirect("movies:list")
    else:
        if flag == 1:
            form = Money.objects.all()
        else:
            form = MoneyCreationForm()
    context = {
        'form':form,
        'flag':flag
    }
    return render(request, 'accounts/money_form.html', context)