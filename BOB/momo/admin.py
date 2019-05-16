from django.contrib import admin
from .models import Movie, Match,UserMatchMoney
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title','poster_url','date']
    search_fields = ['title','date']

admin.site.register(Movie,MovieAdmin)
admin.site.register(Match)
admin.site.register(UserMatchMoney)
