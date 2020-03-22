from audioop import reverse

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from user.froms import UserRegisterForm, RegisterForm, LoginForm
from user.models import UserProfiles
from user.utils import util_sendmsg


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
            # if True:  # 数据校验
            print("1")
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
        return render(request, 'user/register.html', context={'msg': '注册失败'})


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
                login(request, user)  # 将用户保存在底层的request中 (session)
                return redirect('index')
        return render(request, 'user/login.html', context={'errors': lform.errors})


def code_login(request):
    if request.method == "GET":
        return render(request, 'user/codelogin.html')
    else:
        mobile = request.POST.get("mobile")
        code = request.POST.get("code")

        # 根据mobile去session中取值
        check_code = request.session.get(mobile)
        print(check_code)
        if code == check_code:
            return redirect('index')
        else:
            return render(request, 'user/codelogin.html', context={'msg': '验证码有误'})


# 发送验证码路由 axaj发送请求
def send_code(request):
    moblie = request.GET.get('mobile')
    data = {}
    # 取值
    if UserProfiles.objects.filter(mobile=moblie).exists():
        # 发送第三验证码
        json_result = util_sendmsg(moblie)
        print(json_result)
        status = json_result.get('code')
        if status == 200:
            # 在接口返回的json中获取 验证码的值    {'code': 200, 'msg': '8', 'obj': '3928'}
            check_code = json_result.get("obj")
            # 使用session保存
            request.session[moblie] = check_code
            data['status'] = 200
            data['msg'] = '验证码发送成功'
        else:
            data['status'] = 500
            data['msg'] = '验证码发送失败'
    else:
        data['status'] = 501
        data['msg'] = '该用户不存在'

    return JsonResponse(data)


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
