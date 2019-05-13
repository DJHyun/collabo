from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('',views.user_info,name='user_info'),
    path('<int:user_id>/',views.user_detail,name='user_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]