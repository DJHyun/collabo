from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Money,Profile

class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','first_name','last_name']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_num', 'bank','bank_num']

class MoneyCreationForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = ['money']