from audioop import reverse

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user.froms import UserRegisterForm, RegisterForm, LoginForm
from user.models import UserProfiles


def index(request):
    return render(request, 'index.html')


# 注册
def user_register(request):
    if request.method == 'GET':
        # print("请求访问"+str(request))
        return render(request, 'user/register.html')
    else:
        reform = RegisterForm(request.POST)  # 使用form获取数据
        if reform.is_valid():  # 数据校验
            # 取值
            username = reform.cleaned_data.get('username')
            email = reform.cleaned_data.get('email')
            mobile = reform.cleaned_data.get('mobile')
            password = reform.cleaned_data.get('password')
            # 查询
            if not UserProfiles.objects.filter(Q(username=username) | Q(mobile=mobile)).exists():
                # 注册到数据库中
                password = make_password(password)
                user = UserProfiles.objects.create(username=username, password=password, email=email, mobile=mobile)
                if user:
                    return HttpResponse("注册成功")
            else:
                return render(request, 'user/register.html', context={'msg': '用户名或者手机号码已经存在'})
        return render(request, 'user/register.html', context={'msg', '注册失败'})


def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data.get("username")
            password = lform.cleaned_data.get("password")
            # 数据库查询
            # user = UserProfiles.objects.filter(username=username).first()
            # flag = check_password(password, user.password)
            # if flag:
            #     # 保存Session,返回到首页
            #     request.session['username'] = username
            #     return redirect('index')
            #     # 提交时报错    reverse expected 2 arguments, got 1
            #     # return redirect(reverse('index'))

            # 方式二 前提: 使用继承了AbstractUser
            user = authenticate(username=username, password=password)
            if user:
                login(request, user) # 将用户保存在底层的request中 (session)
                return redirect('index')
        return render(request, 'user/login.html', context={'errors': lform.errors})


def user_logout(request):
    # request.session.clear()  # 只删除字典
    # request.session.flush()  # 删除dJango_session表 + cookie + 字典

    # 使用封装好的logout退出
    # Remove the authenticated user's ID from the request and flush their session data.
    logout(request)
    return redirect('index')


def user_zhuce(request):
    if request.method == "GET":
        reform = UserRegisterForm()
        return render(request, 'user/zhuce.html', context={'reform': reform})
    else:
        reform = UserRegisterForm(request.POST)
        # 执行后端校验表单是否符合要求
        if reform.is_valid():
            pass
            # print(reform.cleaned_data)
        return HttpResponse('OK')
