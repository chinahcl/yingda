import base64
import random
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
from django.views import View
from .models import UserProfile
from funit.models import ServiceUnit
import hashlib
from dtoken.views import make_token
from django.core.cache import cache
from django.core.mail import send_mail
# from .tasks import asyn_send_active_email
# from utils.logging_dec import logging_check
from django.conf import settings
from urllib.parse import urlencode
import requests
import logging

log_err=logging.getLogger('err')
log_inf=logging.getLogger('inf')


# 10100 - 10199 异常状态码

# Create your views here.
def users(request):
    print('登录')
    json_str = request.body
    json_obj = json.loads(json_str)
    # {'uname': 'guoxiaonao', 'password': '123456', 'phone': '13488873110', 'email': '250919354@qq.com', 'carts': None}
    username = json_obj['name']
    password = json_obj['password']
    # log_inf.info(f'{username}用户登录')
    log_inf.info(f'{username}用户登录系统')
    print(username, password)
    m = hashlib.md5()
    m.update(password.encode())
    password_m = m.hexdigest()
    # 检查参数
    # 检查用户名是否可用
    old_users = UserProfile.objects.filter(username=username, password=password_m)
    # old_users = UserProfile.objects.filter(username=username, password=password)
    if old_users:
        log_inf.info(f'用户{username}，登录系统成功')
        print('登录成功')
    else:
        log_inf.info(f'用户{username}登录系统失败，用户名密码错')
        result = {'code': 10102, 'error': 'The username is already existed !'}
        return JsonResponse(result)
    # token = make_token(username)
    user_id = old_users.values()[0]['id']
    grade = old_users.values()[0]['grade']
    is_active = old_users.values()[0]['is_active']
    use_unit = old_users.values()[0]['use_unit']
    response = JsonResponse({'code': 10101, 'user': {'userName': username, 'user_id': user_id, "grade": grade, "is_active": is_active, 'use_unit': use_unit}})
    response.set_cookie('username', username, max_age=7 * 24 * 3600)
    request.session['islogin'] = True
    # return JsonResponse({'code':200,'username':username, 'data':{'token':token.decode()}, 'carts_count':0})
    return response


def active_view(request):
    # 获取前端转发的code
    # 校验code
    # code合法 更新用户的is_active
    # 删除redis中对应的key
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'code': 10102, 'error': 'not code'})
    code_str = base64.urlsafe_b64decode(code.encode()).decode()

    random_code, username = code_str.split('_')

    old_code = cache.get("email_active_%s" % (username))
    if not old_code:
        print('???????1')
        return JsonResponse({'code': 10103, 'error': 'The code is error'})

    if old_code != random_code:
        print('???????2')
        return JsonResponse({'code': 10104, 'error': 'The code is error'})

    try:
        print('???????3')
        user = UserProfile.objects.get(username=username, is_active=False)
    except Exception as e:
        print('active error is %s' % (e))
        return JsonResponse({'code': 10105, 'error': 'The username is error'})

    user.is_active = True
    user.save()

    cache.delete("email_active_%s" % (username))

    return JsonResponse({'code': 200, 'data': 'OK'})


# FBV function base view
def address_view(request):
    if request.method == 'GET':
        # 获取地址
        pass

    elif request.method == 'POST':
        # 创建地址
        pass


# CBV class base view
# 按需定义 要使用的method 对应的方法
# 若接收到未定义的动作请求，视图类返回 405响应
def re_grade(grade):
    print(grade,'#######')
    data_info = UserProfile.objects.filter(username=grade)
    print(data_info[0].grade)
    return int(data_info[0].grade) + 1


# 数据图表展示
class tubiao(View):
    def get(self,request):
        print('机器人展示get方法')
        date_str = '机器人展示get方法'
        return date_str

    def post(self,request):
        print('机器人展示post方法')
        date_str = '机器人展示post方法'
        return date_str


# 获取所有用户
class reight(View):
    # resopnse_user = users(request)
    def get(self, request,id):
        print(request.body,id,'%%%%%%%%')
        re_data = []
        if id != 0:
            data_info = UserProfile.objects.filter(use_unit=id)
        else:
            data_info = UserProfile.objects.all()
        for i in data_info.values('id', 'username', 'use_id', 'ment', 'unit_phone', 'chu_name', 'use_iphone',
                                  'use_address',
                                  'use_unit', 'is_active'):
            # print(i['use_unit'])
            try:
                i['unit_id']=i['use_unit']
                i['use_unit'] = ServiceUnit.objects.get(id=i['use_unit']).unit_name
            except Exception as e:
                i['use_unit']= ''
            # print(use_unit.unit_name)
            re_data.append(i)
        re_data_info = {'data': re_data}
        print(re_data_info,"========")
        # log_inf.info('进入查询用户信息页面。。。')
        return JsonResponse(re_data_info)

    def post(self, request):
        print('注册')
        json_str = request.body
        json_obj = json.loads(json_str)['data']
        syx_name = json.loads(json_str)['name']
        print(json_obj,'+++++++')
        # {'uname': 'guoxiaonao', 'password': '123456', 'phone': '13488873110', 'email': '250919354@qq.com', 'carts': None}
        username = json_obj['u_name']
        password = json_obj['password']
        use_id = json_obj['use_id']
        ment = json_obj['ment']
        unit_phone = json_obj['unit_phone']
        chu_name = json_obj['chu_name']
        use_iphone = json_obj['use_iphone']
        use_address = json_obj['use_address']
        use_unit = json_obj['use_unit']
        grade = json_obj['grade']
        grade = re_grade(grade)
        print(username, password)
        # 检查参数
        # 检查用户名是否可用
        old_users = UserProfile.objects.filter(username=username)
        if old_users:
            print("检测用户名是否存在")
            result = {'code': 10100, 'error': 'The username is already existed !'}
            log_inf.info('系统用户'+syx_name+'操作系统，用户名'+username+"已经存在，创建失败！")
            return JsonResponse(result)
        # 创建用户 UserProfile创建数据

        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        try:
            user = UserProfile.objects.create(grade=grade, use_unit=use_unit, username=username, password=password_m,
                                              ment=ment, use_id=use_id, unit_phone=unit_phone, chu_name=chu_name,
                                              use_iphone=use_iphone, use_address=use_address)
            log_inf.info('系统用户'+syx_name+'操作系统，用户：' + str(username) + '，创建成功！')
        except Exception as e:
            print('---user create error is')
            print(e)
            result = {'code': 10101, 'error': 'The username is already existed !'}
            return JsonResponse(result)
        # 签发jwt token(一天)
        token = make_token(username)

        return JsonResponse({'code': 1, 'username': username, 'data': {'token': token.decode()}, 'carts_count': 0})


# 用户编辑
class reight_id(View):
    def post(self, request, id):
        log_inf.info(f'{id}进入编辑')
        print('编辑')
        json_str = request.body
        json_obj = json.loads(json_str)['data']
        sys_name = json.loads(json_str)['name']
        try:
            print(id)
            in_fo = UserProfile.objects.get(id=id)
            old_username = in_fo.username
            print(in_fo.username,'：：原名称')
            in_fo.username = json_obj['username']
            in_fo.use_id = json_obj['use_id']
            # in_fo.unit_phone = json_obj['unit_phone']
            in_fo.unit_phone = json_obj['unit_phone']
            in_fo.chu_name = json_obj['chu_name']
            in_fo.use_iphone = json_obj['use_iphone']
            in_fo.use_address = json_obj['use_address']
            in_fo.ment = json_obj['ment']
            print('现在：',json_obj)
            in_fo.save()
            in_fo.use_unit = ServiceUnit.objects.get(id=in_fo.use_unit).unit_name
            log_inf.info('系统用户'+sys_name+'操作系统，用户：'+old_username+'的信息变更为'+str(json_obj))
            # log_inf.info(f'变更数据{in_fo}')
            print(in_fo)
            return JsonResponse({'code': 1, 'data': {'id':id,'use_unit':in_fo.use_unit,'ment':in_fo.ment,'use_address':in_fo.use_address,'username': in_fo.username,'use_id':in_fo.use_id,'unit_phone':in_fo.unit_phone,'chu_name':in_fo.chu_name,'use_iphone':in_fo.use_iphone}})
        except Exception as e:
            log_inf.info('系统用户'+sys_name+'操作系统，用户'+old_username+"信息修改失败！")
            return JsonResponse({'code': 2})

#用户冻结
class zhengchang(View):
    def get(self, request,id):
        re_data = []
        if id !=0:
            in_fo = UserProfile.objects.filter(is_active=0, use_unit=id)
        else:
            in_fo = UserProfile.objects.filter(is_active=0)
        print(request,'冻结用户get方法')
        for i in in_fo.values('id', 'username', 'use_id', 'ment', 'unit_phone', 'chu_name', 'use_iphone',
                              'use_address',
                              'use_unit', 'is_active'):
            # print(i['use_unit'])
            try:
                i['use_unit'] = ServiceUnit.objects.get(id=i['use_unit']).unit_name
            except Exception as e:
                i['use_unit'] = ''
            # print(use_unit.unit_name)
            re_data.append(i)
        re_data_info = {'data': re_data}
        print('冻结用户：',re_data_info)
        return JsonResponse(re_data_info)

    def post(self, request, id):

        data_info = request.body
        json_obj = json.loads(data_info)['data']
        sys_name = json.loads(data_info)['name']
        print(sys_name)
        # in_fo = UserProfile.objects.get(id=id)
        # json_obj1 = json.loads(data_info)['name']

        # print(json_obj1,'ppppppppp')
        in_fos = UserProfile.objects.filter(is_active=0)
        user_name = ''
        for i in in_fos.values('id', 'username', 'use_id', 'ment', 'unit_phone', 'chu_name', 'use_iphone',
                              'use_address',
                              'use_unit', 'is_active'):
            if i['id'] == id:
                user_name = i['username']
        json_obj = json.loads(data_info)['data']
        in_fo = UserProfile.objects.get(id=id)
        print('is_active', json_obj)
        in_fo.is_active = json_obj
        in_fo.save()
        log_inf.info('系统用户'+sys_name+'操作系统，用户：'+user_name+'状态变更为“冻结”！')
        return JsonResponse({'code': 1})


#用户解冻
class thaw_unit(View):

    def get(self, request,id):
        print("用户解冻get_id：" ,id)
        re_data = []
        if id != 0:
            in_fo = UserProfile.objects.filter(is_active=1, use_unit=id)
        else:
            in_fo = UserProfile.objects.filter(is_active=1)
        print(in_fo)
        for i in in_fo.values('id', 'username', 'use_id', 'ment', 'unit_phone', 'chu_name', 'use_iphone',
                              'use_address',
                              'use_unit', 'is_active'):
            print('use_unit:',i['use_unit'])
            # i['use_unit'] = ServiceUnit.objects.get(id=i['use_unit']).unit_name
            # print(use_unit.unit_name)
            re_data.append(i)
        re_data_info = {'data': re_data}
        return JsonResponse(re_data_info)

    def post(self, request, id):
        print("用户解冻post_id：",id)
        data_info = request.body
        sys_name = json.loads(data_info)['name']
        print(data_info)
        user_name = ''
        in_fos = UserProfile.objects.filter(is_active=1)
        for i in in_fos.values('id', 'username', 'use_id', 'ment', 'unit_phone', 'chu_name', 'use_iphone',
                              'use_address',
                              'use_unit', 'is_active'):
            if i['id']==id:
                user_name = i['username']
        json_obj = json.loads(data_info)['data']
        in_fo = UserProfile.objects.get(id=id)
        print('json_obj', json_obj)
        in_fo.is_active = json_obj
        in_fo.save()
        log_inf.info('系统用户'+sys_name+'操作系统，用户：' + user_name + '状态变更为“解冻”！')
        return JsonResponse({'code': 1})