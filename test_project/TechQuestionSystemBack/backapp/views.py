from django.shortcuts import render, redirect
from django.views import View

from backapp.forms import ArticleForm, CategoryForm
from backapp.models import ArticleModel, CategoryModel


class Index(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回管理后台首页
        article_count = ArticleModel.objects.filter(a_status=1).count()
        return render(request, 'index.html', {'article_count': article_count})


class Article(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回文章列表页
        articles = ArticleModel.objects.all()
        return render(request, 'article.html', {'articles': articles})


class AddArticle(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回文章列表页
        categorys = CategoryModel.objects.all()
        return render(request, 'add_article.html', {'categorys': categorys})

    def post(self, request, *args, **kwargs):
        # 校验文章上传的字段，是否通过form表单验证
        form = ArticleForm(request.POST)
        if form.is_valid():
            # 表单验证通过，则创建
            ArticleModel.objects.create(**form.cleaned_data)
            return redirect('backapp:article')
        else:
            # 如果表单验证失败，则form的错误信息，错误信息为form.errors
            categorys = CategoryModel.objects.all()
            return render(request, 'add_article.html', {'categorys': categorys, 'form': form})


class UpdateArticle(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        # 获取需要更新的文章信息
        article = ArticleModel.objects.filter(id=id).first()
        # 获取栏目分类
        categorys = CategoryModel.objects.all()
        return render(request, 'add_article.html', {'article': article, 'categorys': categorys})

    def post(self, request, *args, **kwargs):
        # 校验文章上传的字段，是否通过form表单验证
        form = ArticleForm(request.POST)
        if form.is_valid():
            id = kwargs['id']
            # 表单验证通过，则更新
            ArticleModel.objects.filter(id=id).update(**form.cleaned_data)
            return redirect('backapp:article')
        else:
            # 如果表单验证失败，则form的错误信息，错误信息为form.errors
            categorys = CategoryModel.objects.all()
            article = ArticleModel.objects.filter(id=id).first()
            return render(request, 'add_article.html', {'categorys': categorys,
                                                        'form': form,
                                                        'article': article})


class Category(View):
    def get(self, request, *args, **kwargs):
        # 判断如果是get请求，则返回栏目添加页
        categorys = CategoryModel.objects.all()
        return render(request, 'category.html', {'categorys': categorys})

    def post(self, request, *args, **kwargs):
        # 使用表单校验
        form = CategoryForm(request.POST)
        # 通过判断is_valid()方法，如果返回为True，则表示form表单验证通过
        if form.is_valid():
            # 校验成功，则创建栏目
            CategoryModel.objects.create(**form.cleaned_data)
            # 栏目创建成功，则跳转到栏目的列表页面
            return redirect('backapp:category')
        else:
            # 如果验证不通过，则返回当前页面，并返回form表单的错误信息
            categorys = CategoryModel.objects.all()
            return render(request, 'category.html', {'categorys': categorys, 'form': form})


class UpdateCategory(View):
    def get(self, request, *args, **kwargs):
        # 获取栏目id
        id = kwargs['id']
        # 查询栏目对象
        category = CategoryModel.objects.filter(id=id).first()
        # 查询父栏目
        categorys = CategoryModel.objects.filter(c_child=None)
        return render(request, 'update_category.html', {'category': category, 'categorys': categorys})

    def post(self, request, *args, **kwargs):
        # 使用表单校验
        form = CategoryForm(request.POST)
        # 通过判断is_valid()方法，如果返回为True，则表示form表单验证通过
        if form.is_valid():
            id = kwargs['id']
            # 校验成功，则更新栏目
            CategoryModel.objects.filter(id=id).update(**form.cleaned_data)
        return redirect('backapp:category')


class DeleteCategory(View):
    def get(self, request, *args, **kwargs):
        # 获取栏目id
        id = kwargs['id']
        # 删除栏目
        CategoryModel.objects.filter(id=id).delete()
        return redirect('backapp:category')
