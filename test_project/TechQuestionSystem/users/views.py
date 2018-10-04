import json
import re
from datetime import timedelta, datetime

from django.core import serializers
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users.forms import UserLoginForm, UserRegisterForm
from users.models import UserModel, VerifyCodeModel, UserLeavingMessage
from utils.functions import get_verify_code
from utils.sms.send_message import msg


class Login(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回登录页面
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = UserLoginForm(data)
        if form.is_valid():
            # 1. 验证表单成功，获取用户信息
            name_mobile = form.cleaned_data['name_mobile']
            user = UserModel.objects.filter(Q(username=name_mobile) | Q(mobile=name_mobile)).first()
            # 修改session中的登录状态
            request.session['user_id'] = user.id
            return redirect('/')
        else:
            # 如果表单验证不成功，则可以从form.errors中获取到验证失败的错误信息
            return render(request, 'login.html', {'form': form, 'data': data})


class Logout(View):

    def get(self, request, *args, **kwargs):
        # 设置session中用户的登录状态为false
        request.session.clear()
        # 注销跳转到首页
        return redirect('/')


class Register(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回注册页面
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        # 获取post请求中传递的参数
        data = request.POST
        # 使用表单验证，如果form表单验证成功，则is_valid()为True，反之为False
        form = UserRegisterForm(data)
        if form.is_valid():
            # 表单验证成功以后，可以通过form的cleaned_data方法获取参数值
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            mobile = form.cleaned_data['mobile']
            # 保存用户信息，并且对密码加密
            UserModel.objects.create(username=username, password=make_password(password), mobile=mobile)
            # 验证表单成功，保存用户信息成功，则跳转到商城首页
            return redirect('users:login')
        else:
            # 如果表单验证不成功，则可以从form.errors中获取到验证失败的错误信息
            return render(request, 'register.html', {'form': form, 'data': data})


class UserStatus(View):
    def get(self, request, *args, **kwargs):
        # 获取当前登录系统的用户信息
        user_id = request.session.get('user_id')
        if user_id:
            user = UserModel.objects.filter(id=user_id)
            # 序列化用户信息
            user_info = serializers.serialize('json', user, fields=('id', 'username'))
            user_info = json.loads(user_info)
            return JsonResponse({'code': 200, 'msg': '请求成功', 'data': user_info})
        else:
            return JsonResponse({'code': 1004, 'msg': '用户没有登录'})


class LeavingMsg(View):
    def post(self, request, *args, **kwargs):
        # 文章id，用户id，内容
        article_id = kwargs['id']
        user_id = request.session.get('user_id')
        content = request.POST.get('content')
        # 评论的父id
        fid = request.POST.get('fid')
        if content:
            UserLeavingMessage.objects.create(user_id=user_id, article_id=article_id,
                                              message=content, user_msg_id=fid)
        # 带参数的跳转要使用reverse()
        return redirect(reverse('home:detail', kwargs={'id': article_id}))


class SendMsg(View):

    def post(self, request, *args, **kwargs):
        mobile = request.POST.get('mobile')
        # 校验手机号码是否符合规范
        if not re.match(r'^1[345678]\d{9}$', mobile):
            return JsonResponse({'code': 1001, 'msg': '手机号不正确'})
        # 验证手机是否已经注册过
        if UserModel.objects.filter(mobile=mobile).count():
            raise JsonResponse({'code': 1002, 'msg': '该手机号已经注册'})
        # 验证是否已经发送过验证码
        if VerifyCodeModel.objects.filter(mobile=mobile):
            # 如果已经发送过验证码，则验证发送频率
            one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
            if VerifyCodeModel.objects.filter(create_time__gt=one_minutes_ago):
                # 验证码没超过一分钟
                return JsonResponse({'code': 1003, 'msg': '发送验证码没有超过60s，请稍后再试'})
            else:
                # 验证码超过一分钟
                code = get_verify_code()
                VerifyCodeModel.objects.filter(mobile=mobile).update(code=code, create_time=datetime.now())
                # 发送验证码
                msg(code, mobile)
                return JsonResponse({'code': 200, 'msg': '发送验证码成功', 'data': {'code': code}})
        else:
            code = get_verify_code()
            VerifyCodeModel.objects.create(mobile=mobile, code=code)
            # 发送验证码
            msg(code, mobile)
            return JsonResponse({'code': 200, 'msg': '发送验证码成功', 'data': {'code': code}})