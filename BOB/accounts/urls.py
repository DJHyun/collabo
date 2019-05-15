from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('',views.user_info,name='user_info'),
    path('<int:user_id>/',views.user_detail,name='user_detail'),
    path('<int:user_id>/update/', views.user_update, name='user_update'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:match_id>/up/', views.up_money, name='up_money'),
    path('<int:match_id>/down/', views.down_money, name='down_money'),
    path('money/<int:flag>/<int:user_id>', views.money, name='money'),
    # path('purchase/<int:match_id>/<int:point>/<int:updown_code>/',views.purchase,name="purchase"),
    path('purchase/<int:match_id>/',views.purchase,name="purchase"),
    path('refund/<int:match_id>/',views.refund,name="refund"),
    path('check/<int:check_num>/<int:money_id>/', views.check_b, name="check"),
    path('payment/<int:user_id>/', views.payment, name='payment'),
    path('exchange/<int:user_id>/', views.exchange, name='exchange'),
]