from rest_framework import serializers  # from django import forms 와 비슷
from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        field = ('__all__')