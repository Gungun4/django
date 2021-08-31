from django.urls import path, re_path
from . import views

urlpatterns = [
    path('all_book', views.all_book)
]