import hashlib
import json
import random
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from .models import UserProfile, Blog, Comment
from tools.logging_dec import logging_check
from tools.sms import YunTongXin
from django_redis import get_redis_connection
from tools.cache_handle import check_code
# Create your views here.
from .tasks import send_sms, fixed_time_blog

# django提供了一个装饰器 method_decorator 可以将函数装饰器转换成 类方法装饰器
conn = get_redis_connection('default')

def task_test(request):
    result = fixed_time_blog.delay()
    return JsonResponse(result)


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


def sms_views(request):
    if request.method != "POST":
        result = {'code': 10106, 'error': 'please use post'}
        return JsonResponse(result)

    json_obj = json.loads(request.body)
    phone = json_obj['phone']

    code = ''
    for i in range(6):
        code += str(random.randint(0, 9))
    send_sms.delay(phone, code)
    conn.set(phone, code, 300)

    return JsonResponse({'code': 200, 'data': {}})


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
                'info': user.info, 'sign': user.sign, 'nickname': user.nickname, 'avatar': str(user.avatar)}}
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
        sms_num = json_obj['sms_num']

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
    def put(self, request, username=None):
        # 更新个人数据
        json_str = request.body
        json_obj = json.loads(json_str)

        user = request.myuser
        user.sign = json_obj['sign']
        user.info = json_obj['info']
        user.nickname = json_obj['nickname']
        user.save()
        return JsonResponse({'code': 200})


class BlogViews(View):

    @method_decorator(logging_check)
    def get(self, request, username=None, t_id=None):
        # get username blog

        user = UserProfile.objects.get(username=username)
        if username != request.myuser.username:
            user_blogs = Blog.objects.filter(user_profile_username_id=username,
                                             is_active=True).order_by('-id')
        else:
            user_blogs = Blog.objects.filter(user_profile_username_id=username).order_by('-id')
        print('-------------------', t_id, '--------------------------')
        if t_id:
            user_blog = Blog.objects.get(id=t_id)
            messages = Comment.objects.filter(blog_id=t_id)

            message_list = []
            for i in messages:
                dic = i.__dict__
                del dic['_state']
                message_list.append(i.__dict__)

            last_id = user_blogs.filter(id__lt=t_id)
            next_id = user_blogs.filter(id__gt=t_id)

            result = {
                'code': 200,
                'data': {
                    'nickname': user.nickname,
                    'messages': message_list,
                    'title': user_blog.title,
                    'created_time': user_blog.created_time,
                    'category': user_blog.category,
                    'introduce': user.info,
                    'content': user_blog.content,
                    'messages_count': messages.count(),
                }
            }
            if last_id:
                last_id = last_id[0]
                result['data']['last_id'] = last_id.id
                result['data']['last_title'] = last_id.title
            if next_id:
                next_id = next_id[0]
                result['data']['next_id'] = next_id.id
                result['data']['next_title'] = next_id.title
            return JsonResponse(result)
        blog_list = []
        for i in user_blogs:
            dic = i.__dict__
            del dic['_state']
            blog_list.append(i.__dict__)
        # print(blog_list)
        result = {
            'code': 200,
            'data': {
                'nickname': user.nickname,
                'topics': blog_list
            }
        }
        return JsonResponse(result)

    @method_decorator(logging_check)
    def post(self, request, username=None):
        # create blog
        json_obj = json.loads(request.body)
        title = json_obj['title']
        if not title:
            return JsonResponse({'code': 10202, 'error': 'title is not be null'})
        content = json_obj['content_text']
        user = request.myuser.username
        is_active = [True if json_obj['limit'] == 'public' else False]
        category = json_obj['category']
        # title - ----123456789 - ----zsw - ----[True] - ----tec
        print(title, content, user, is_active, category, sep='-----')
        Blog.objects.create(title=title,
                            content=content,
                            user_profile_username_id=user,
                            is_active=is_active[0],
                            category=category)
        return JsonResponse({'code': 200, 'data': {}})

    def put(self, request):
        # update blog
        pass

    @method_decorator(logging_check)
    def delete(self, request, username=None, t_id=None):
        if username == request.myuser.username:
            Blog.objects.get(id=int(t_id)).delete()
            return JsonResponse({'code': 200, 'data': {}})
        return JsonResponse({'code': 10105, 'error': '非法请求'})
        pass


class CommentViews(View):

    def get(self, request):
        pass

    @method_decorator(logging_check)
    def post(self, request, t_id=None):
        if t_id:
            json_obj = json.loads(request.body)
            user = request.myuser.username
            text = json_obj['content']
            Comment.objects.create(text=text, blog_id=t_id, user_profile_username_id=user)
            return JsonResponse({'code': 200, 'data': {}})
        return JsonResponse({'code': 10404, 'error': 't_id is null'})
        pass
