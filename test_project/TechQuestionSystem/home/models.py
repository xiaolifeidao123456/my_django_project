from django.db import models

"""
定义基础模型
"""
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    operate_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        abstract = True


"""
定义栏目模型
"""
class CategoryModel(BaseModel):
    c_title = models.CharField(max_length=30, verbose_name='标题')
    c_child = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.CASCADE, verbose_name='自我关联')

    class Meta:
        db_table = 't_category'


"""
文章模型
"""
class ArticleModel(BaseModel):
    a_title = models.CharField(max_length=30, verbose_name='文章标题')
    a_desc = models.CharField(max_length=100, verbose_name='文章描述')
    a_content = models.TextField(verbose_name='文章内容')
    a_category = models.ForeignKey(CategoryModel, verbose_name='article', null=True, blank=True, on_delete=models.SET_NULL)
    a_tag = models.CharField(max_length=30, verbose_name='标签')
    # 发布状态，为1表示发布，为0表示不发布
    a_status = models.BooleanField(default=1, verbose_name='发布状态')

    class Meta:
        db_table = 't_article'
