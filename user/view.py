from captcha.models import CaptchaStore
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from user.froms import UserRegisterForm, RegisterForm, LoginForm, CaptchaTestForm
from user.models import UserProfiles
from user.utils import util_sendmsg, send_email, upload_image


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
            # 从前台获取input值
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


# 用户账号密码登录
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


# 用户验证码登录
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
            # 验证码匹配后根据手机号获取user对象数据
            user = UserProfiles.objects.filter(mobile=mobile).first()
            # 认证 如果合法 返回User对象, 如果不合法返回None
            # 认证给出的用户名和密码，使用 authenticate() 函数。它接受两个参数，用户名 username 和 密码 password ，
            # 并在密码对给出的用户名合法的情况下返回一个 User 对象。 如果密码不合法，authenticate()返回None。
            # https://www.cnblogs.com/ccorz/p/6357815.html

            # 该user.password 的是来自于数据中查询得到的明文password 和认证的password不一致
            # user = authenticate(username=user.username, password=user.password)
            if user:
                # authenticate() 只是验证一个用户的证书而已。 而要登录一个用户，使用 login() 。
                # 该函数接受一个 HttpRequest 对象和一个 User 对象作为参数并使用Django的会话（ session ）框架把用户的ID保存在该会话中。
                login(request, user)
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


# 忘记密码
def forget_password(request):
    if request.method == "GET":
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})
    else:
        # 发送邮件
        email = request.POST.get("email")
        # 给此邮箱发送邮件
        result = send_email(email, request)
        if result:
            return HttpResponse("邮件发送成功！赶快去邮箱更改密码！<a href='/'>返回首页>>> </a>")


# 更新密码
def update_pwd(request):
    if request.method == "GET":
        #根据邮件发送获取的ID
        c = request.GET.get("c")
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        code = request.POST.get('code')
        uid = request.session.get(code)
        user = UserProfiles.objects.get(pk=uid)
        # 获取密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd == repwd and user:
            # 加密
            pwd = make_password(pwd)
            user.password = pwd
            user.save()
            return render(request, 'user/update_pwd.html', context={'msg': '密码更新成功'})
        else:
            return render(request, 'user/update_pwd.html', context={'msg': '更新失败'})


# 定义一个路由验证码
def valide_code(request):
    if request.is_ajax():
        key = request.GET.get('key')
        code = request.GET.get('code')
        captcha = CaptchaStore.objects.filter(hashkey=key).first()
        if captcha.response == code.lower():
            data = {'status': 1}
        else:
            data = {'status': 0}
        return JsonResponse(data)
    else:
        pass


# 用户退出登录
def user_logout(request):
    # request.session.clear()  # 只删除字典
    # request.session.flush()  # 删除dJango_session表 + cookie + 字典

    # 使用封装好的logout退出
    # Remove the authenticated user's ID from the request and flush their session data.
    logout(request)
    return redirect('index')


#用户的个人中心
@login_required     #装饰器,  login(request,user) user -> 继承自 abstractuser
def user_center(request):
    user = request.user
    if request.method == "GET":
        return render(request, 'user/center.html', context={"user": user})
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        icon = request.FILES.get("icon")
        # 更新信息
        user.username = username
        user.email = email
        user.mobile = mobile
        user.icon = icon
        user.save()
        return render(request, 'user/center.html', context={"user": user})


#用户的个人中心 -> 使用七牛云存储
@login_required     #装饰器,  login(request,user) user -> 继承自 abstractuser
def user_center1(request):
    user = request.user
    if request.method == "GET":
        return render(request, 'user/center.html', context={"user": user})
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        icon = request.FILES.get("icon")
        # 更新信息
        user.username = username
        user.email = email
        user.mobile = mobile
        user.icon = icon
        user.save()

        # 上传到七牛云
        # save_path = upload_image(icon, str(user.icon))
        save_path = upload_image(icon)
        user.yunicon = save_path
        user.save()

        return render(request, 'user/center.html', context={"user": user})

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
