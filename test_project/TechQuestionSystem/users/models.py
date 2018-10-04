from django.db import models

from home.models import ArticleModel, BaseModel


class UserModel(BaseModel):
    """
     用户表
    """
    username = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="姓名")
    password = models.CharField(max_length=255, verbose_name="密码")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    is_delete = models.BooleanField(default=0, verbose_name='是否被禁用')

    class Meta:
        db_table = 't_user'


class UserLeavingMessage(BaseModel):
    """
    用户留言表
    """
    user = models.ForeignKey(UserModel, verbose_name='用户', on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleModel, verbose_name='文章', on_delete=models.CASCADE)
    message = models.TextField(default='', verbose_name='留言内容')
    user_msg = models.ForeignKey('self', verbose_name='自关联', null=True, blank=True, related_name='child', on_delete=models.CASCADE)
    is_show = models.BooleanField(default=0, verbose_name='是否展示')

    class Meta:
        db_table = 't_user_leaving_message'


class VerifyCodeModel(BaseModel):
    """
    发送短信验证码的验证
    """
    code = models.CharField(max_length=8, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')

    class Meta:
        db_table = 't_verify_code'
