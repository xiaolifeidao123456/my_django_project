
from django import forms

from backapp.models import CategoryModel, ArticleModel

"""
栏目form表单
"""
class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = '__all__'

"""
文章form表单
"""
class ArticleForm(forms.ModelForm):
    class Meta:
        model = ArticleModel
        fields = '__all__'
