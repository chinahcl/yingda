
import base64
import random

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json

from django.views import View

from login.models import UserProfile
import hashlib
from dtoken.views import make_token
from django.core.cache import cache
from django.core.mail import send_mail
# from .tasks import asyn_send_active_email
# from utils.logging_dec import logging_check
from django.conf import settings
from urllib.parse import urlencode
import requests


#10100 - 10199 异常状态码

# Create your views here.
def users(request):
    print('注册')
    json_str = request.body
    json_obj = json.loads(json_str)
    #{'uname': 'guoxiaonao', 'password': '123456', 'phone': '13488873110', 'email': '250919354@qq.com', 'carts': None}
    username = json_obj['name']
    password = json_obj['password']
    phone = json_obj['phone']
    department = json_obj['department']
    print(username,password,phone,department)
    #检查参数
    #检查用户名是否可用
    old_users = UserProfile.objects.filter(phone=phone)
    if old_users:
        print(1111)
        result = {'code':10100, 'error': 'The username is already existed !'}
        return JsonResponse(result)
    #创建用户 UserProfile创建数据

    m = hashlib.md5()
    m.update(password.encode())
    password_m = m.hexdigest()
    try:
        user = UserProfile.objects.create(username=username,password=password_m,phone=phone,department=department)
    except Exception as e:
        print('---user create error is')
        print(e)
        result = {'code': 10101, 'error': 'The username is already existed !'}
        return JsonResponse(result)
    #签发jwt token(一天)
    token = make_token(username)
    return JsonResponse({'code':200,'username':username, 'data':{'token':token.decode()}, 'carts_count':0})





def active_view(request):
    #获取前端转发的code
    #校验code
    #code合法 更新用户的is_active
    #删除redis中对应的key
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'code':10102, 'error':'not code'})
    code_str = base64.urlsafe_b64decode(code.encode()).decode()

    random_code, username = code_str.split('_')

    old_code = cache.get("email_active_%s"%(username))
    if not old_code:
        return JsonResponse({'code':10103, 'error':'The code is error'})

    if old_code != random_code:
        return JsonResponse({'code':10104, 'error':'The code is error'})

    try:
        user = UserProfile.objects.get(username=username, is_active=False)
    except Exception as e:
        print('active error is %s'%(e))
        return JsonResponse({'code': 10105, 'error': 'The username is error'})

    user.is_active = True
    user.save()

    cache.delete("email_active_%s"%(username))

    return JsonResponse({'code':200, 'data':'OK'})


#FBV function base view
def address_view(request):

    if request.method == 'GET':
        #获取地址
        pass

    elif request.method == 'POST':
        #创建地址
        pass


#CBV class base view
# 按需定义 要使用的method 对应的方法
# 若接收到未定义的动作请求，视图类返回 405响应

