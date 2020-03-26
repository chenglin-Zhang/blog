
media文件: 文件上传的文件

模型: FileField(任何文件) ImgageFiled(只能是图片)

FileField(upload_to='表示文件上传路径' , uploads/%Y/%m/%d)

此路径是基于media_root指明的路径:
    MEDIA_URL = '/static/media'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

模板中如果使用引用上传的文件,并显示:
    就需要再setting.py 添加 .media




系统默认用户的几重使用

    1.必须继承AbstractUser
    2.必修修改setting.py
    3.执行迁移和同步

forms 表单

    Django会处理涉及表单的三个不同部分:
        准备并重组数据, 以便下一步选人
        为数据创建Html表单,
        接收并处理客户端提交的表单数据


session的使用:

    request.session

    设置session的值
    request.session['key'] =value

    取值
    value = request.session.get(key)

    删除aa
    request.session.clear()
    request.session.flush()
    request.session[key] # 删除指定的key


继承了AbstractUser

    logout() 注销用户

    authenticate + login() 在数据库中执行数据查询,如果有返回用户对象
    login(request,user) 类似于session

    request.user.is_authenticated 是否是认证过的用户返回值是True, False
 
 
发送手机验证码: 第三方

    发送验证码:
    
    验证码登录
    

使用插件captcha验证码

    1. pip install django-simple-captcha
    2.setting.yp > INSTALL_APPS 添加 captcha
    3.运行 python manage.py migrate       在库中添加了captcha表
    4.urls.py中添加entry
    

中间件:
    
    进行用户的登录验证
    1.中间件的请求路径验证用户登录
        步骤:
        1. 文件夹 -> xxxmiddleware.py -> 定义类继承MiddlewareMixin
        2. 重写:
            
            
            
云存储:
    
    1.注册用户
    2.创建存储空间
    3.文档中心
    4.项目中使用