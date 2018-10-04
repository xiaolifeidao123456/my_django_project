import re
from datetime import datetime, timedelta

from django import forms
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator
from django.db.models import Q

from users.models import UserModel, VerifyCodeModel


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, min_length=5,
                               error_messages={'required': '请输入5-20个字符的用户名',
                                               'max_length': '用户名不能超过20个字符',
                                               'min_length': '用户名不能少于5个字符'}
                               )
    password = forms.CharField(required=True, max_length=20, min_length=8,
                               error_messages={'required': '密码最少8位，最长20位',
                                               'max_length': '最长20位',
                                               'min_length': '密码最少8位'}
                               )
    # 短信验证码验证字段
    # mobile_msg = forms.CharField(required=True, error_messages={'required': '验证码必填'})
    mobile = forms.CharField(required=True, error_messages={'required': '手机号码必填'},
                             validators=[RegexValidator(r'^1[34578]\d{9}$', '请填写正确的手机号')])
    password2 = forms.CharField(required=True, error_messages={'required':'确认密码必填'})
    allow = forms.BooleanField(required=True, error_messages={'required':'请勾选同意'})

    def clean(self):
        # 获取用户名和密码
        username = self.cleaned_data.get('username')
        # 验证用户名是否存在
        user = UserModel.objects.filter(username=username).first()
        if user:
            # 如果用户名存在，则提示用户名已存在
            raise forms.ValidationError({'username': '用户名已存在'})
        # # 校验验证码是否正确
        # verify_code = VerifyCodeModel.objects.filter(mobile=self.cleaned_data['mobile']).first()
        # if verify_code:
        #     # 判断输入的验证码是否正确
        #     if verify_code.code != self.cleaned_data['mobile_msg']:
        #         raise forms.ValidationError({'mobile': '验证码不正确'})
        # else:
        #     # 手机号不正确
        #     raise forms.ValidationError({'mobile': '手机号码不正确'})

        return self.cleaned_data


class UserLoginForm(forms.Form):
    name_mobile = forms.CharField(required=True,
                                  error_messages={'required': '用户名/手机号必填'})
    password = forms.CharField(required=True,
                               error_messages={'required': '密码必填'})

    def clean(self):
        # 获取用户名/手机和密码
        name_mobile = self.cleaned_data.get('name_mobile')
        password = self.cleaned_data.get('password')
        # 验证用户名/手机是否存在
        user = UserModel.objects.filter(Q(username=name_mobile) | Q(mobile=name_mobile)).first()
        if not user:
            # 如果用户名不存在，则提示先注册
            raise forms.ValidationError({'name_mobile':'用户名/手机不存在，请先注册'})

        # 验证用户名是否正确
        if not check_password(password, user.password):
            raise forms.ValidationError({'password':'密码错误'})

        return self.cleaned_data
