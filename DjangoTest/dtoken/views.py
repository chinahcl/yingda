import hashlib

from django.http import JsonResponse
from django.shortcuts import render
import json
from login.models import UserProfile
import time
from django.conf import settings
# from carts.views import CartsView


#10200 - 10299 异常状态码

# Create your views here.
def tokens(request):

    #{"username":"guoxiaonao","password":"123456","carts":null}
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj['username']
    password = json_obj['password']

    #参数检查

    #获取用户
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        print('--get user error is')
        print(e)
        result = {'code':10200, 'error': 'The username or password is wrong'}
        return JsonResponse(result)

    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        result = {'code': 10201, 'error': 'The username or password is wrong'}
        return JsonResponse(result)

    #签发token
    token = make_token(username)
    result = {'code':200, 'username':username, 'data':{'token':token.decode()}, 'carts_count':0}

    #合并购物车
    # carts_data = json_obj.get('carts')
    # carts_obj = CartsView()
    # carts_len = carts_obj.merge_carts(user.id, carts_data)
    # result['carts_count'] = carts_len

    return JsonResponse(result)



def make_token(username, expire=3600*24):
    import jwt
    now = time.time()
    payload = {'username':username, 'exp': int(now + expire)}
    key = settings.JWT_TOKEN_KEY
    return jwt.encode(payload, key, algorithm='HS256')

