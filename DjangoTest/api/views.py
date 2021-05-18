import hashlib

from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import User_user_table
# Create your views here.
def findUserName(request):
    print('验证用户名')
    json_str = request.body
    json_obj = json.loads(json_str)
    #{'uname': 'guoxiaonao', 'password': '123456', 'phone': '13488873110', 'email': '250919354@qq.com', 'carts': None}
    username = json_obj['userName']
    # password = json_obj['password']
    # phone = json_obj['phone']
    # department = json_obj['department']
    # print(username,password,phone,department)
    #检查参数
    #检查用户名是否可用
    old_users = User_user_table.objects.filter(username=username)
    if old_users:
        print(1111)
        result = {'code':'002','msg':'用户名重复'}
        return JsonResponse(result)
    else:
        result = {'code': '001', 'msg': '可用'}
        return JsonResponse(result)
    #创建用户 UserProfile创建数据

    # m = hashlib.md5()
    # m.update(password.encode())
    # password_m = m.hexdigest()
    # try:
    #     user = User_user_table.objects.create(username=username,password=password_m,department=department)
    # except Exception as e:
    #     print('---user create error is')
    #     print(e)
    #     result = {'code': 10101, 'error': 'The username is already existed !'}
    #     return JsonResponse(result)
    # #签发jwt token(一天)
    # # token = make_token(username)
    # return JsonResponse({'code':'001','username':username, 'data':{'token':token.decode()}, 'carts_count':0})
    # return JsonResponse({'code':'002','msg':'可用'})


def register(request):
    print('验证用户名')
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['userName']
    password = json_obj['password']
    department='0'
    # phone = json_obj['phone']
    # department = json_obj['department']
    # print(username,password,phone,department)
    # 检查参数
    # 检查用户名是否可用
    m = hashlib.md5()
    m.update(password.encode())
    password_m = m.hexdigest()
    try:
        user = User_user_table.objects.create(username=username,password=password_m,department=department)

    except Exception as e:
        print('---user create error is')
        print(e)
        result = {'code': 10101, 'error': '注册失败，请再次尝试!'}
        return JsonResponse(result)
        # #签发jwt token(一天)
        # # token = make_token(username)
        # return JsonResponse({'code':'001','username':username, 'data':{'token':token.decode()}, 'carts_count':0})
    return JsonResponse({'code':'001','msg':'注册成功！'})


def login(request):
    print('登录')
    json_str = request.body
    print(json_str)
    json_obj = json.loads(json_str)
    print(json_obj)
    # {'uname': 'guoxiaonao', 'password': '123456', 'phone': '13488873110', 'email': '250919354@qq.com', 'carts': None}
    username = json_obj['userName']
    password = json_obj['password']
    print(username, password)
    m = hashlib.md5()
    m.update(password.encode())
    password_m = m.hexdigest()
    # 检查参数
    # 检查用户名是否可用
    old_users = User_user_table.objects.filter(username=username, password=password_m)
    try:
        user_id=old_users.values()[0]['id']
    except Exception as e:
        return JsonResponse({'code': 10102, 'msg': '用户名密码错！'})
    # print(old_users.list())
    if old_users:
        response = JsonResponse({'code': '001','user': {'userName': username,'user_id':user_id}})
        response.set_cookie('username', username, max_age=1 * 24 * 3600)
        response.set_cookie('password', password, max_age=1 * 24 * 3600)
        request.session['islogin'] = True
        print(username+'登录成功')
        return response
    else:
        result = {'code': 10101, 'msg': '用户名密码错！'}
        return JsonResponse(result)
    # return JsonResponse({'code': '001', 'user': {'user_id':user_id, 'userName': username }, 'msg': '登录成功！', 'session.username':username ,'carts_count': 0})


def all_info(request):
    print('返回所有值')
    response = JsonResponse({'code': '001', 'data': [{'unit_name':'杨健','unit_abb':'2','use':'3','phone':'4','iphone':'5','address':'22222'},{'unit_name':'4','unit_abb':'2','use':'3','phone':'4','iphone':'5','address':'22222'},{'unit_name':'4','unit_abb':'2','use':'3','phone':'4','iphone':'5','address':'22222'}]})
    return response


def single_add_unit(request):
    json_str = request.body
    print(json_str,"====++++")
    json_obj = json.loads(json_str)
    print(json_obj)
    return None