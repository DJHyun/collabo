from django.contrib import admin
from .models import Movie, Match,UserMatchMoney
# Register your models here.

admin.site.register(Movie)
admin.site.register(Match)
admin.site.register(UserMatchMoney)
