from gungunblog.celery import app
from tools.sms import YunTongXin
import time
from .models import Blog

@app.task
def send_sms(phone, code):
    config = {
        "accountSid": '8aaf07087b9a3d03017ba0580a97014f',
        "accountToken": '6728df5319e24808a73c5dbb6dd0c7eb',
        "appId": '8aaf07087b9a3d03017ba0580b880155',
        "templateId": '1'
    }
    print(config)
    return phone
    # yun = YunTongXin(**config)
    # res = yun.run(phone, code)

@app.task()
def fixed_time_blog():
    result = {
        'code': 200,
        'data': {
            'nickname': 'user.nickname',
            'topics': 'blog_list'
        }
    }
    return result