from django.db import models
import random


def default_sign():
    signs = ['come on boy', 'come on girl']
    return random.choice(signs)


# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=11, verbose_name='username', primary_key=True)
    nickname = models.CharField(max_length=30, verbose_name='nickname')
    password = models.CharField(max_length=32)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='avatar', null=True)
    sign = models.CharField(max_length=50, verbose_name='', default=default_sign)
    info = models.CharField(max_length=150, verbose_name='', default='')
    sex_choice = ((0, 'woman'), (1, 'man'))
    sex = models.IntegerField(choices=sex_choice, default=1)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_user_profile'


class Blog(models.Model):
    user_profile_username = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, verbose_name='title', null=False)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    is_technology = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    category_choice = (('tec', '技术'), ('game', '游戏'), ('news', '新闻'), ('sports', '体育'))
    category = models.CharField(max_length=11, choices=category_choice, default='tec')
    img = models.ImageField(upload_to='blog_img',null=True)

    class Meta:
        db_table = 'user_blog'


class Comment(models.Model):
    text = models.TextField()
    likes = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    user_profile_username = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_comment'
