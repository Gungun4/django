import paramiko.dsskey
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
import hashlib
from .function import *
from django.core.paginator import Paginator
from django.core.cache import cache
import csv, json
from django_redis import get_redis_connection

conn = get_redis_connection('default')


def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('login')
            else:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)

    return wrap


# Create your views here.
def index(request):
    return render(request, 'user/index.html')


def logout(request):
    if request.session.get('username'):
        # del request.session['username']
        request.session.flush()

    resp = HttpResponseRedirect('index')
    if request.COOKIES.get('username'):
        resp.delete_cookie('username')
        resp.delete_cookie('uid')
    return resp


def login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')

    if request.method == 'POST':
        print(request.POST, '----------')
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(name=username)
        except Exception as e:
            print(e)
            return HttpResponse('uname or password error')

        m = hashlib.md5()
        m.update(password.encode('utf8'))

        if m.hexdigest() != user.password:
            return HttpResponse('uname or password error')

        # 存session
        request.session['username'] = username
        request.session['uid'] = user.id

        resp = HttpResponseRedirect('index')
        # 存cookie
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600 * 24 * 3)
            resp.set_cookie('uid', user.id, 3600 * 24 * 3)

        return resp


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'user/sign_in.html')

    if request.method == 'POST':
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            checkpwd = request.POST.get('checkpwd', '1')
            check = User.objects.filter(name=username)

            if check:
                return HttpResponse('User name already exists')

            elif not check and password == checkpwd:
                m = hashlib.md5()
                m.update(password.encode('utf8'))
                password_m = m.hexdigest()
                user = User.objects.create(name=username, password=password_m)
                request.session['username'] = username
                request.session['uid'] = user.id
                return HttpResponseRedirect('login')
        except Exception as msg:
            logger(msg)
            return HttpResponseRedirect('sign_in')

    pass


@check_login
def note(request):
    uid = request.session.get('uid')

    if not uid:
        return HttpResponseRedirect('login')
    if request.method == "GET":
        page_num = request.GET.get('page', 1)
        logger(page_num)
        notes = Paginator(Note.objects.filter(user=uid), 10)
        try:
            c_page = notes.page(int(page_num))
        except Exception as e:
            logger(e)
            c_page = notes.page(1)
    return render(request, 'user/note.html', locals())


@check_login
def note_add(request, uid=None):
    uid = request.session['uid']

    if request.method == "GET":
        if uid:
            cont = {}
            cont['id'] = int(uid)
            try:
                cont['note'] = Note.objects.get(id=int(uid))
            except Exception as e:
                logger(e)
                return redirect('note')
            return render(request, 'user/note_add.html', cont)
        return render(request, 'user/note_add.html')

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        file = request.FILES.get('name', None)
        logger('--------------------------')
        if title:
            try:
                if id:
                    Note.objects.filter(id=int(id)).update(title=title, content=content)
                    UploadFile.objects.filter(user_id=uid).update(file_path=file)
                else:
                    UploadFile.objects.create(info=title, file_path=file, user_id=uid)
                    Note.objects.create(title=title, content=content, user_id=uid)
            except Exception as e:
                logger(e)
                return HttpResponse('fail')
        else:
            return HttpResponse('"title con not be null"')
        # return HttpResponseRedirect('note')
        return redirect('note')


@check_login
def note_del(request, uid):
    uid = int(uid)

    try:
        Note.objects.filter(id=uid).delete()
    except Exception as e:
        logger(e)
        return redirect('note')
    return redirect('note')


def create_csv(request):
    uid = request.session['uid']
    page_num = request.GET.get('page', 1)
    notes = Paginator(Note.objects.filter(user=uid), 2)
    data = notes.page(int(page_num)).object_list
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment;filename="1.csv"'
    write = csv.writer(response)
    for b in data:
        logger(b.__dict__)
        write.writerow(b.__dict__.values())
    return response


@check_login
def info(request, uid):
    cache_key = f"user:{uid}"
    if request.method == 'GET':

        if conn.exists(cache_key):
            u = conn.hgetall(cache_key)
            user = {k.decode(): v.decode() for k, v in u.items()}
            logger('redis', user)
            return render(request, 'user/userinfo.html', locals())

        try:
            user = User.objects.get(id=int(uid))
        except Exception as e:
            logger(e)
        logger('mysql', user)
        u = {'name':user.name,"desc":user.desc}
        conn.hmset(cache_key,u)
        return render(request, 'user/userinfo.html', locals())

    if request.method == "POST":
        name = request.POST['uname']
        desc = request.POST['uinfo']
        user = User.objects.filter(id=int(uid))
        user.update(name=name, desc=desc)
        conn.delete(cache_key)
        url = f'{uid}'
        return HttpResponseRedirect(url)
        pass
