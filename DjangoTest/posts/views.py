from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
import urllib.parse,os,json
from funit.models import ServiceUnit
import pandas as pd

# Create your views here.
# def upload(request):
#     print(request.FILES.get('file'))
#     return JsonResponse({'code':1})

import logging

log_err=logging.getLogger('err')
log_inf=logging.getLogger('inf')

class MyModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        for i in request.FILES:
            print(i)
        print(json.loads(request.data)['name'],'ppp')
        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid(raise_exception=False)
        if not is_valid:
            return Response({'code': 0, 'msg': '失败', 'data': serializer.errors})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        path2 = urllib.parse.unquote(serializer.data['file'].split('/')[-1])
        path1 = os.getcwd()
        path = r'{0}\upload\upload\{1}'.format(path1, path2)
        read_excel(path)
        print(serializer.data,"----------------")
        log_inf.info('系统用户：'+json.loads(request.data)['name']+'批量上传服务单位成功！')
        return Response({'code': 1, 'msg': '成功','data':serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        is_valid = serializer.is_valid(raise_exception=False)
        if not is_valid:
            return Response({'code': 0, 'msg': '失败', 'data': serializer.errors})
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        print(serializer.data,'成功，2============')
        return Response({'code': 1, 'msg': '成功','data':serializer.data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(serializer.data,'3===========')
            return self.get_paginated_response({'code': 1, 'msg': '成功','data':serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for i in data:
            i['w_name'] = urllib.parse.unquote(i['file'].split('/')[-1])
            print(i['w_name'],"*******")
        print(data,'4============')
        return Response({'code': 1, 'msg': '成功','data':data})

#上传下载
class FilViewSet(MyModelViewSet):
    print(11111,'000000')
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer


#单位写进数据库
def crete_execl(json_obj):
    ServiceUnit.objects.create(unit_name=json_obj['unit_name'], unit_abb=json_obj['unit_abb'],
                                           use=json_obj['use'], phone=json_obj['phone'], iphone=json_obj['iphone'],
                                           address=json_obj['address'], userxu=json_obj['userxu'],
                                           uintstate=json_obj['uintstate'])


# @transaction.atomic
def read_excel(path):
    print("post-read_excel......")
    #重复的单位
    cunit = []
    #重复和不重复的单位
    bunit = []
    #所有的单位
    units = []
    names = ServiceUnit.objects.values('unit_name')
    namess = {ii['unit_name'] for ii in names}
    c_data = pd.read_excel(path)
    for i in c_data.values:
        data_dict = {}
        data_dict['unit_name'] = i[1]
        data_dict['unit_abb'] = i[2]
        data_dict['use'] = i[3]
        data_dict['phone'] = i[4]
        data_dict['iphone'] = i[5]
        data_dict['address'] = i[6]
        data_dict['userxu'] = 1
        data_dict['uintstate'] = 1
        if data_dict['unit_name'] in namess:
            cunit.append(data_dict['unit_name'])
            bunit.append({'name':data_dict['unit_name'],'state':'flase'})
            print('5=========')
        else:
            bunit.append({'name':data_dict['unit_name'],'state':'单位名称不重复'})
            print('6=========')
        units.append(data_dict)
    if len(cunit) == 0:
        for ii in units:
            crete_execl(ii)
    json_str = json.dumps(bunit)
    path1 = os.getcwd()
    with open(r'{}\upload\json\test_data.json'.format(path1), 'w') as json_file:
        json_file.write(json_str)
