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
