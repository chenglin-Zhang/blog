import hashlib
import json
from time import time

import requests


# 想网易云信发送请求
def util_sendmsg(mobile):
    #网易云信
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

    #json
    str_result = response.text #获取相应体内容
    json_result= json.loads(str_result) #转换为json
    return json_result