# 绝对导入，以免celery和标准库中的celery模块冲突
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# 以下导入时为了确保在Django启动时加载app，shared_task在app中会使用到
from .celery import app as celery_app

__all__ = ['celery_app']
