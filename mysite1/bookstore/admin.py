from django.contrib import admin
from .models import Book, Author


# Register your models here.


# 模型管理器类
class BookManager(admin.ModelAdmin):
    # 列表页显示那些字段的页
    list_display = ['id', 'title', 'pub', 'price', 'market_price']

    # 控制list_display 那些字段可以链接到修改页
    list_display_links = ['title']

    # 添加过滤器
    list_filter = ['id']

    # 添加搜索框（模糊查询）
    search_fields = ['title']

    # 添加可在列表页可编辑的字段
    list_editable = ['price','market_price']


class AuthorManager(admin.ModelAdmin):

    list_display = ['id','name' , 'age', 'email']


# 注册模型类和模型管理器绑定
admin.site.register(Book, BookManager)
admin.site.register(Author, AuthorManager)
