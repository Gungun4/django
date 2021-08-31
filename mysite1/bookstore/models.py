from django.db import models


# Create your models here.

# 一个类对应一个表，一个类属性对应一个字段
class Book(models.Model):
    title = models.CharField('bookname', max_length=50, default='', unique=True)
    pub = models.CharField('pub', max_length=100, default='')
    price = models.DecimalField('price', max_digits=7, decimal_places=2, default=0.0)
    market_price = models.DecimalField('market', max_digits=7, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE)

    class Meta:
        # 设置表在数据库中的名称（不设置默认为应用名 + _ + 小写类名)
        db_table = 'book'
        # 设置模型类在admin后台显示的名称
        verbose_name = '图书'
        # 复数
        verbose_name_plural = verbose_name


class Author(models.Model):
    name = models.CharField(max_length=11)
    age = models.IntegerField(default=1)
    email = models.EmailField(null=True)

    # author = models.ForeignKey(primary_key=True, to='Book', to_field='id', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'author'


class Husband(models.Model):
    name = models.CharField(max_length=11)


class Wife(models.Model):
    name = models.CharField(max_length=11)
    husband = models.OneToOneField(to="Husband", on_delete=models.CASCADE)
