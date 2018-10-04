from django.urls import path, re_path

from home import views

urlpatterns = [
    # 办理后台首页
    path('index/', views.Index.as_view(), name='index'),
    # 详情页
    path('detail/<int:id>/', views.ArticleDetail.as_view(), name='detail'),
    # 分类列表
    path('list/<int:id>/', views.ArticleList.as_view(), name='list'),
    # 联系我们
    path('contact/', views.Contact.as_view(), name='contact'),
    # 搜索
    path('search/', views.Search.as_view(), name='search'),
]
