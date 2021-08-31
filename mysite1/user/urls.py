from . import views
from django.urls import path, re_path

urlpatterns = [
    path('index', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('sign_in', views.sign_in, name='signin'),
    path('note', views.note, name='note'),
    path('note_add', views.note_add, name='note_add'),
    re_path(r'^note_del/(?P<uid>\d+)', views.note_del, name='note_del'),
    re_path(r'^note_edit/(?P<uid>\d+)$', views.note_add, name='note_edit'),
    re_path(r'^info/(?P<uid>\d+)$',views.info,name='info'),
    path('create_csv',views.create_csv)
]
