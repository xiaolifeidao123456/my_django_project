from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from TechQuestionSystem.settings import PAGE_NUMBER
from home.models import ArticleModel, CategoryModel
from users.models import UserLeavingMessage


class Index(View):
    def get(self, request, *args, **kwargs):
        # 特色考题

        # 最新考题
        new_articles = ArticleModel.objects.order_by('-id')[:10]
        return render(request, 'index.html', {'new_articles': new_articles})


class ArticleDetail(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        # 查询指定id的文章信息
        article = ArticleModel.objects.filter(id=id).first()
        # 获取栏目分类
        categorys = CategoryModel.objects.order_by('id')
        # 留言信息, 查找根留言信息
        leaving_msgs = UserLeavingMessage.objects.filter(article_id=id, user_msg=None, is_show=1)
        return render(request, 'single.html', {'article': article, 'categorys': categorys,
                                               'leaving_msgs': leaving_msgs})


class ArticleList(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        try:
            # 获取分页
            page = request.GET.get('page', 1)
        except:
            page = 1
        # 查询指定id的文章信息
        articles = ArticleModel.objects.filter(a_status=1, a_category=id)
        # 实现分页
        paginator = Paginator(articles, PAGE_NUMBER)
        page = paginator.page(page)
        # 获取栏目分类
        categorys = CategoryModel.objects.order_by('id')
        return render(request, 'articles_list.html', {'page': page, 'categorys': categorys})


class Contact(View):
    def get(self, request, *args, **kwargs):
        # 返回联系页面
        return render(request, 'contact.html')


class Search(View):
    def get(self, request, *args, **kwargs):
        try:
            # 获取分页
            page = request.GET.get('page', 1)
        except:
            page = 1
        search_msg = request.GET.get('search_msg')
        # 对搜索文章标题进行模糊搜索
        articles = ArticleModel.objects.filter(a_title__icontains=search_msg)
        # 获取栏目分类
        categorys = CategoryModel.objects.order_by('id')
        # 实现分页
        paginator = Paginator(articles, PAGE_NUMBER)
        page = paginator.page(page)
        return render(request, 'articles_list.html', {'page': page,
                                                      'search_msg': search_msg,
                                                      'categorys': categorys})
