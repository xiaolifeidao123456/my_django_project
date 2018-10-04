
from django.contrib import auth
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserLoginForm


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # 使用auth，验证用户名和密码是否正确
            user = auth.authenticate(request,
                                     username=request.POST.get('username'),
                                     password=request.POST.get('password'))
            if user:
                # 如果验证用户成功，则获取到user对象，并使用Djnaog自带的auth的login方法实现登录
                auth.login(request, user)
                return redirect('backapp:index')
            else:
                # 如果校验用户失败，则跳转到登录页面并提示用户名或者密码错误
                return render(request, 'login.html', {'errors': '用户名或者密码错误'})
        else:
            return render(request, 'login.html', {'form': form})


class Logout(View):
    def get(self, request, *args, **kwargs):
        # 使用django自带的auth的logout方法，实现退出操作
        auth.logout(request)
        return redirect('back:login')
