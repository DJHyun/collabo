from django import forms
from .models import Score

class ScoreForm(forms.ModelForm):
    content = forms.CharField(max_length=120)
    value = forms.IntegerField()
    class Meta:
        model = Score
        fields = ['content','value',]