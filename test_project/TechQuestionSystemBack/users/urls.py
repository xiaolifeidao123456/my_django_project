from django.contrib.auth.decorators import login_required
from django.urls import path

from users import views

urlpatterns = [
    # 登录
    path('login/', views.Login.as_view(), name='login'),
    # 退出
    path('logout/', login_required(views.Logout.as_view()), name='logout'),
]
