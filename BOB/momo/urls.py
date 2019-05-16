from django.urls import path
from . import views

app_name="movies"

urlpatterns = [
    path('', views.test),
    path('list/',views.movieList,name="list"),
    path('predict/',views.predict,name="predict"),
    path('getdata/',views.getmoviedatalocal,name="getdata"),
    path('history/',views.history,name="history"),
]