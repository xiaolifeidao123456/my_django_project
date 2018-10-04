from django.contrib.auth.decorators import login_required
from django.urls import path

from backapp import views

urlpatterns = [
    # 办理后台首页
    path('index/', login_required(views.Index.as_view()), name='index'),
    # 文章列表
    path('article/', login_required(views.Article.as_view()), name='article'),
    # 添加文章
    path('add_article/', login_required(views.AddArticle.as_view()), name='add_article'),
    # 修改文章
    path('update_article/<int:id>/', login_required(views.UpdateArticle.as_view()), name='update_article'),

    # 栏目
    path('category/', login_required(views.Category.as_view()), name='category'),
    # 修改栏目
    path('update_category/<int:id>/', login_required(views.UpdateCategory.as_view()), name='update_category'),
    # 删除栏目
    path('delete_category/<int:id>/', login_required(views.DeleteCategory.as_view()), name='delete_category'),
]
