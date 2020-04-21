import re

from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, EmailField
from django import forms

from user.models import UserProfiles


class UserRegisterForm(Form):
    username = forms.CharField(max_length=15, min_length=4, required=True, error_messages={'max_length': '用户名不能超过16位'},
                               label='用户名')
    email = forms.EmailField(required=True, error_messages={'required': '请填写邮箱'}, label='邮箱')
    mobile = forms.CharField(required=True, error_messages={'required': '请填写手机'}, label='手机')
    password = forms.CharField(required=True, error_messages={'required': '请填写密码'}, label='密码',
                               widget=forms.widgets.PasswordInput)

    # 检验
    def clean_username(self):
        username = self.cleaned_data.get("username")
        result = re.match(r'[a-zA-Z]\w{5,}', username)
        if not result:
            raise ValidationError("用户名必须首字母开头")
        return username


class RegisterForm(ModelForm):
    # repassword = forms.CharField(required=True, error_messages={'required': '请填写密码'}, label='确认密码', widget=forms.widgets.PasswordInput)
    class Meta:
        model = UserProfiles
        fields = ['username', 'email', 'mobile', 'password']


class LoginForm(Form):
    username = forms.CharField(max_length=15, min_length=4, required=True, error_messages={'max_length': '用户名不能超过16位'},
                               label='用户名')
    password = forms.CharField(required=True, error_messages={'required': '请填写密码'}, label='密码',
                               widget=forms.widgets.PasswordInput)

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if not UserProfiles.objects.filter(username=username).exists():
    #         raise ValidationError('用户名不正确')


# 验证码captcha的From
class CaptchaTestForm(Form):
    email = forms.EmailField(required=True, label="邮箱", error_messages={'requited': '必须填写邮箱'})
    captcha = CaptchaField()
