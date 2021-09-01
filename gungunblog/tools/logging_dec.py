import time

import jwt
from django.http import JsonResponse

from user.models import UserProfile


def logging_check(func):
    def wrap(request, *args, **kwargs):
        # 获取token request.META.get('HTTP_AUTHORIZATION')
        # 校验token
        # 失败 ，code 403 error please login
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            result = {'code': 403, 'error': 'please login'}

        key = '123456'  # 也可以配置在settings.py中

        try:
            res = jwt.decode(token, key)
        except Exception as e:
            print(f'jwt decode error is {e}')
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        username = res['username']
        user = UserProfile.objects.get(username=username)
        request.myuser = user
        return func(request, *args, **kwargs)

    return wrap
