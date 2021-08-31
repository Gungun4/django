"""mysite1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # 主路由
    path('admin/', admin.site.urls),
    path('',views.index_view),
    re_path(r'^birthday/(?P<y>\d{4})/(?P<m>\d{1,2})/(?P<d>\d{1,2})$',views.birthday_view),
    re_path(r'^birthday/(?P<m>\d{1,2})/(?P<d>\d{1,2})/(?P<y>\d{4})$',views.birthday_view),
    path('page/1',views.page_view),
    path('redirect',views.redirect_view),
    path('test_html',views.test_html),
    path('match',views.match_view,name='match'),
    path('play',views.play_view,name='play'),
    path('set_cookies',views.set_cookies),
    path('set_session',views.set_session),
    path('get_session',views.get_session),

    # 分布应用路由
    path('music/', include('music.urls')),
    path('bookstore/', include('bookstore.urls')),
    path('user/', include('user.urls')),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)