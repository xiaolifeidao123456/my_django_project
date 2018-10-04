from django.urls import path

from users import views

urlpatterns = [
    # 登录
    path('login/', views.Login.as_view(), name='login'),
    # 注册
    path('register/', views.Register.as_view(), name='register'),
    # 退出
    path('logout/', views.Logout.as_view(), name='logout'),
    # 全局获取用户的状态
    path('user_status/', views.UserStatus.as_view(), name='user_status'),
    # 留言
    path('leaving_msg/<int:id>/', views.LeavingMsg.as_view(), name='leaving_msg'),
    # 发送验证码
    path('send_msg/', views.SendMsg.as_view(), name='send_msg'),
]