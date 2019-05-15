from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Money

class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','first_name','last_name','bank']

class MoneyCreationForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = ['money']