from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render


def index_view(request):
    dic = {}
    return render(request, 'home.html', dic)


def birthday_view(request, y, m, d):
    html = f'your birthday is {y}.{m}.{d}'
    return HttpResponse(html)


def page_view(request):
    html = f'page 1'
    return HttpResponse(html)


# 重定向
def redirect_view(request):
    html = f'redirect'
    return HttpResponseRedirect('/page/1')


def test_ger_post(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
    else:
        pass

    return HttpResponse('--test get post is ok--')


def test_html(request):
    dic = {
        "username": ["zsw", 19980709],
        "password": "zxc"
    }
    print(locals())
    return render(request, 'test.html', locals())


def match_view(request, time=0, flag=False):
    if flag:
        return HttpResponseRedirect('/play')
    else:
        return render(request, 'matching.html', locals())


def play_view(request):
    return render(request, 'play.html')


def set_cookies(request):
    resp = HttpResponse('set cookies is ok')
    resp.set_cookie('uuname', 'gxn', 3600)
    return resp


def set_session(request):
    request.session['uname'] = 'zsw'
    return HttpResponse('set session is ok')


def get_session(request):
    value = request.session.get('uname', 'zxc')
    return HttpResponse('session is %s' % (value))
