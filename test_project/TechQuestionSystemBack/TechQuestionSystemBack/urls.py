"""TechQuestionSystemBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from django.views.static import serve

from TechQuestionSystemBack import settings
from backapp import views
from utils.upload_images import upload_image

urlpatterns = [
    # 管理后台user方法
    path('back/', include(('users.urls', 'users'), namespace='back')),
    # 管理后台backapp路由规则
    path('backapp/', include(('backapp.urls', 'backapp'), namespace='backapp')),
    # kindeditor编辑器上传图片地址
    re_path(r'^util/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),

    # 配置media路径
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 访问'/'地址，跳转到管理后台的index方法
    re_path(r'^$', login_required(views.Index.as_view()), name='index'),
]
