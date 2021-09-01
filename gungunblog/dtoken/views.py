import hashlib
import json
import time
import jwt
from django.shortcuts import render
from django.http import JsonResponse
from user.models import UserProfile


# Create your views here.
# faid code 10200-10300

def tokens(request):
    if request.method != 'POST':
        result = {'code': 10200, 'error': 'please use post!'}
        return JsonResponse(result)
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password = json_obj['password']

    try:
        user = UserProfile.objects.get(username=username)
        m = hashlib.md5()
        m.update(password.encode('utf8'))
        if m.hexdigest() != user.password:
            return JsonResponse({"code": 10200, "error": '帐户或密码不正确'})
    except Exception as e:
        return JsonResponse({"code": 10200, "error": '帐户或密码不正确'})
    token = make_token(username)
    result = {"code": 200, "username": username, "data": {"token": token.decode('utf8')}}
    return JsonResponse(result)


def make_token(username, expire=3600 * 24):
    key = '123456'  # 也可以配置在settings.py中
    now_t = time.time()
    payload_data = {'username': username, 'exp': now_t + expire}
    return jwt.encode(payload_data, key, algorithm='HS256')
