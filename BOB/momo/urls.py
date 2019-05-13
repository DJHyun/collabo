from django.urls import path
from . import views

urlpatterns = [
    path('', views.test),
    path('list/',views.movieList)
]