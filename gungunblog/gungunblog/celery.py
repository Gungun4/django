from celery import Celery
from django.conf import settings
import os

# celery在一个服务器里面可以起多个 在linux环境变量里面加一个特殊的环境变量 设置celery可以在命令行中使用
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gungunblog.settings')

app = Celery('gungunblog')

app.config_from_object('django.conf:settings',namespace='CELERY')

# 自动去注册应用下寻找加载worker函数
app.autodiscover_tasks(settings.INSTALLED_APPS)
