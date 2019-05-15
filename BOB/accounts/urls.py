from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('',views.user_info,name='user_info'),
    path('<int:user_id>/',views.user_detail,name='user_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:match_id>/up/', views.up_money, name='up_money'),
    path('<int:match_id>/down/', views.down_money, name='down_money'),
    path('money/<int:flag>/<int:user_id>', views.money, name='money'),
]