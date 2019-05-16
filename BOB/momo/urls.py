from django.urls import path
from . import views

app_name="movies"

urlpatterns = [
    path('', views.test),
    path('list/',views.movieList,name="list"),
    path('predict/',views.predict,name="predict"),
    path('getdata/',views.getmoviedatalocal,name="getdata"),
    path('<int:match_id>/scores/new/', views.create_score, name='create_score'),
    path('<int:match_id>/scores/<int:score_id>/delete/', views.score_delete, name='score_delete'),
    # path('momodetail/<int:match_id>/',views.momodetail,name="momodetail"),
    # path('<int:match_id>/scores/', views.create_score, name='create_score'),
    # path('scores/<int:score_pk>/', views.score, name='score_delete'),
]