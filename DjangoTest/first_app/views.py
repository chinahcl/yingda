from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# from django_redis.serializers import json
import json


def one_web(request):
    print('第一页')
    json_str = request.body
    json_obj = json.loads(json_str)
    print(json_obj)
    return JsonResponse({'code':200,'username':'eeeeeeee'})