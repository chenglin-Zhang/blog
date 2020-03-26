import hashlib
import json
import uuid
from time import time
import smtplib
from email.mime.text import MIMEText
import requests

# 想网易云信发送请求
from django.core.mail import send_mail

from dJan.settings import EMAIL_HOST_USER
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
    print(email)
    subject = '找回密码'
    user = UserProfiles.objects.filter(email=email).first()
    ran_code = uuid.uuid4()
    print(ran_code)
    ran_code = str(ran_code)
    print(type(ran_code))
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
