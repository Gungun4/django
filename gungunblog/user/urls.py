from . import views
from django.urls import path, re_path

urlpatterns = [
    path('<str:username>', views.UserViews.as_view()),
    path('<str:username>/avatar',views.user_views),
]
