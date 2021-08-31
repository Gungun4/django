import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import UserProfile


# Create your views here.


def user_views(request):
    if request.method == 'GET':
        pass

    if request.method == "POST":
        pass


class UserViews(View):

    def get(self, request):
        return JsonResponse({"code": 200, 'msg': "test"})

    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)

        username = json_obj['username']
        email = json_obj['email']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        phone = json_obj['phone']
        result = {"code": 200, "content": {}, "error": {}}
        return JsonResponse(result)
