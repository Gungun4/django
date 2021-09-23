from . import views
from django.urls import path, re_path

urlpatterns = [
    path('task',views.task_test),
    # topics/zsw/2
    re_path('^topics/(?P<username>\w+)/(?P<t_id>\d+)$', views.BlogViews.as_view()),
    path('topics/<str:username>', views.BlogViews.as_view()),
    path('messages/<int:t_id>',views.CommentViews.as_view()),
    path('sms', views.sms_views),
    path('<str:username>', views.UserViews.as_view()),
    path('<str:username>/avatar', views.user_views),

]
