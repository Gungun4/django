import hashlib
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from tools.logging_dec import logging_check
from .models import UserProfile
# Create your views here.

# django提供了一个装饰器 method_decorator 可以将函数装饰器转换成 类方法装饰器


# FBV
@logging_check
def user_views(request, username):
    # 上传头像
    if request.method != "POST":
        result = {'code': 10103, 'error': 'please use post'}
        return JsonResponse(result)
    user = request.myuser
    avatar = request.FILES['avatar']
    user.avatar = avatar
    user.save()
    return JsonResponse({'code': 200})

# CBV
class UserViews(View):

    def get(self, request, username=None):
        if username:
            try:
                print(username)
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                print(e)
                result = {'code': 10102, "error": 'the username is wrong'}
                return JsonResponse(result)
            result = {'code': 200, 'username': username, 'data': {
                'info': user.info,'sign':user.sign, 'nickname': user.nickname, 'avatar': str(user.avatar)}}
            return JsonResponse(result)
        else:
            return JsonResponse({"code": 200, 'msg': "test"})

    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        phone = json_obj['phone']
        if password_1 != password_2:
            return JsonResponse({'code': 10210, 'error': 'The two passwords are inconsistent '})
        m = hashlib.md5()
        m.update(password_1.encode('utf8'))
        try:
            UserProfile.objects.get(username=username)
            result = {"code": 10200, "error": 'this username is exist'}
            return JsonResponse(result)
        except Exception as e:
            UserProfile.objects.create(username=username, nickname=username, email=email,
                                       password=m.hexdigest(), phone=phone)
        result = {"code": 200, 'username': username}
        return JsonResponse(result)

    @method_decorator(logging_check)
    def put(self,request,username=None):
        # 更新个人数据
        json_str = request.body
        json_obj = json.loads(json_str)

        user = request.myuser
        user.sign = json_obj['sign']
        user.info = json_obj['info']
        user.nickname = json_obj['nickname']
        user.save()
        return JsonResponse({'code': 200})
