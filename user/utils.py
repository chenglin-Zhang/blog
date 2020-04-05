import hashlib
import json
import os
import uuid
from time import time
import smtplib
from email.mime.text import MIMEText
import requests

# 想网易云信发送请求
from django.core.mail import send_mail
from qiniu import Auth, put_file, put_data

from dJan.settings import EMAIL_HOST_USER, MEDIA_ROOT
from user.models import UserProfiles


def util_sendmsg(mobile):
    # 网易云信  接口地址: https://dev.yunxin.163.com/docs/product/%E7%9F%AD%E4%BF%A1/%E7%9F%AD%E4%BF%A1%E6%8E%A5%E5%8F%A3%E6%8C%87%E5%8D%97
    url = 'https://api.netease.im/sms/sendcode.action'
    data = {'mobile': mobile}
    # 四部分组成 appkey None CurTime CheckSum
    AppKey = '4c1cb5c5ec7f5373a19049de8060a20c'
    Nonce = '102310923lkd'
    CurTime = str(time())
    AppSecret = '530101bb72af'
    content = AppSecret + Nonce + CurTime
    # 用hashlib的sha1加密,  hexdest()转化为16进制
    CheckSum = hashlib.sha1(content.encode("UTF-8")).hexdigest()

    headers = {'AppKey': AppKey, 'Nonce': Nonce, 'CurTime': CurTime, 'CheckSum': CheckSum}
    # requests---> 相当于创建了一个浏览器,通过url访问这个网站
    response = requests.post(url, data, headers=headers)

    # json
    str_result = response.text  # 获取相应体内容
    json_result = json.loads(str_result)  # 转换为json
    return json_result


# 邮件发送
def send_email(email, request):
    subject = '找回密码'
    user = UserProfiles.objects.filter(email=email).first()
    ran_code = uuid.uuid4()
    ran_code = str(ran_code)
    ran_code = ran_code.replace('-', '')
    request.session[ran_code] = user.id
    message = '''
        Dear,
            User, 此链接用于用户找回密码,<a href='http://127.0.0.1:8000/user/update_pwd?c=%s'>更新密码</a>
            如果链接不能点击,请复制:
            http://127.0.0.1:8000/user/update_pwd?c=%s
        个人博客团队
    ''' % (ran_code, ran_code)
    result = send_mail(subject, message, EMAIL_HOST_USER, [email, ], html_message = message)
    return result


#上传图片到七牛云
# def upload_image(storeobj, imagepath):
def upload_image(storeobj):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'Y8tTQJqYZDl1KMD8pqDlrPIQTmZN-bJV928bwRhT'
    secret_key = 'enUCVLEpa-9eRfnWcxp8OaRIkf2oZqJvieYDH9fP'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'cheng-django'

    # 上传后保存的文件名
    key = storeobj.name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = os.path.join(MEDIA_ROOT, imagepath)
    '''
        UPDATA BY Cheng START
        Error: put_file改为put_data
        put_file: 在本地存储时使用put_file找到文件
        put_data: 文件以二进制的方式存储
        上传文档参考: https://developer.qiniu.com/kodo/sdk/1242/python
    '''
    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, storeobj.read())
    '''
        UPDATA BY Cheng END
    '''
    print(ret, info)
    filename = ret.get('key')
    save_path = 'http://q7slh7oqx.bkt.clouddn.com/' + filename
    return save_path