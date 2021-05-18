from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from robot.models import RobotInfo
from .models import *
from django.db.models import Q
from django.views import View
from django.core import serializers
import json
import logging
log_err=logging.getLogger('err')
log_inf=logging.getLogger('inf')


# 服务单位信息
class MyModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        # json_str=request.body
        # reque=json.loads(json_str)
        print(request.data['data'])
        serializer = self.get_serializer(data=request.data['data'])
        is_valid = serializer.is_valid(raise_exception=False)
        if not is_valid:
            return Response({'code': 0, 'msg': '失败', 'data': serializer.errors})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'code': 1, 'msg': '成功', 'data': serializer.data}, status=status.HTTP_201_CREATED,
                        headers=headers)

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

        return Response({'code': 1, 'msg': '成功', 'data': serializer.data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'code': 1, 'msg': '成功', 'data': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'code': 1, 'msg': '成功', 'data': serializer.data})


class Uint(MyModelViewSet):
    serializer_class = UnitSerializer

    def get_queryset(self):
        unit_name = self.request.query_params.get('key', False)
        if unit_name:
            queryset = ServiceUnit.objects.filter(Q(unit_name=unit_name) | Q(unit_abb=unit_name) | Q(id=unit_name))
        else:
            queryset = ServiceUnit.objects.all()
        return queryset

    queryset = ServiceUnit.objects.all()

#单笔增加单位、查询
class Test(View):
    def get(self, request):
        print('单位查询，修改前：',request.body)
        re_data = []
        data_info = ServiceUnit.objects.all()
        for i in data_info.values('id', 'unit_name', 'unit_abb', 'use', 'phone', 'iphone', 'address', 'uintstate',
                                  'userxu'):
            re_data.append(i)
        re_data_info = {'data': re_data}
        return JsonResponse(re_data_info)

    def post(self, request, id=0):
        data_info = request.body
        sys_name = json.loads(data_info)['name']
        json_obj = json.loads(data_info)['data']
        print(json_obj)
        if id != 0:
            unit_name = ''
            try:
                print(id)
                in_fo = ServiceUnit.objects.get(id=id)
                data_info = ServiceUnit.objects.all()

                for i in data_info.values('id', 'unit_name', 'unit_abb', 'use', 'phone', 'iphone', 'address',
                                          'uintstate',
                                          'userxu'):
                    if i['id'] == id:
                        unit_name = i['unit_name']
                print(in_fo,"unit_name名称为："+unit_name)
                in_fo.address = json_obj['address']
                in_fo.iphone = json_obj['iphone']
                in_fo.phone = json_obj['phone']
                in_fo.unit_abb = json_obj['unit_abb']
                in_fo.unit_name = json_obj['unit_name']
                in_fo.use = json_obj['use']
                in_fo.save()
                print('----->>>>>in_fo',json_obj)
                log_inf.info('系统用户'+sys_name+'操作系统，服务单位“'+unit_name+'”信息变更为：'+str(json_obj))
                return JsonResponse({'code': 1})
            except Exception as e:
                log_err.error('系统用户' + sys_name + '操作系统，服务单位’' + unit_name + '‘信息变更失败！')
                return JsonResponse({'code': 2})
        else:
            print('创建')
            try:
                data_info = ServiceUnit.objects.create(unit_name=json_obj['unit_name'], unit_abb=json_obj['unit_abb'],
                                                       use=json_obj['use'], phone=json_obj['phone'],
                                                       iphone=json_obj['iphone'], address=json_obj['address'],
                                                       userxu=json_obj['userxu'], uintstate=json_obj['uintstate'])
                print(data_info)
                log_inf.info(f'系统用户{json_obj["name"]}操作系统，创建单笔服务单位，名称{json_obj["unit_name"]},添加成功')
                return JsonResponse({'code': 1})
            except Exception as e:
                log_err.error(f'系统用户{json_obj["name"]}操作系统，创建单笔服务单位，名称{json_obj["unit_name"]},添加失败,账号重复')
                return JsonResponse({'code': 2})


# 获取非冻结状态下的数据
class fronzen_unit(View):
    def get(self, request):
        w = 1
        re_data = []
        data_info = ServiceUnit.objects.filter(userxu='1')
        for i in data_info.values('id', 'unit_name', 'unit_abb', 'use', 'phone', 'iphone', 'address', 'uintstate',
                                  'userxu'):
            i['unit_index'] = w
            re_data.append(i)
            w += 1
        re_data_info = {'data': re_data}
        return JsonResponse(re_data_info)

    def post(self, request, id):
        data_info = request.body
        json_obj = json.loads(data_info)['data']
        json_obj_name = json.loads(data_info)['name']
        in_fo = ServiceUnit.objects.get(id=id)
        print('json_obj', json_obj)
        in_fo.userxu = json_obj
        in_fo.save()
        unit_status = ''
        if json_obj == 1:
            unit_status = '解冻'
        else:
            unit_status = '冻结'
        log_inf.info(f'系统用户{json_obj_name}操作系统，变更用户:{in_fo.unit_name}为“'+unit_status+'”状态')
        return JsonResponse({'code': 1})


# 获取非冻结状态下的数据
class thaw_unit(View):
    def get(self, request):
        re_data = []
        data_info = ServiceUnit.objects.filter(userxu='2')
        for i in data_info.values('id', 'unit_name', 'unit_abb', 'use', 'phone', 'iphone', 'address', 'uintstate',
                                  'userxu'):
            re_data.append(i)
        re_data_info = {'data': re_data}
        return JsonResponse(re_data_info)

    def post(self, request, id):
        data_info = request.body
        json_obj = json.loads(data_info)['data']
        in_fo = ServiceUnit.objects.get(id=id)
        print('json_obj：：：', json_obj)
        in_fo.userxu = json_obj
        in_fo.save()
        return JsonResponse({'code': 1})


# 获取单位名称unit_name
class unit_name(View):
    def get(self, request,id):
        print('单位名称')
        print(id)
        re_data = []
        if id != 0:
            data_info = ServiceUnit.objects.filter(userxu=1,id=id)
        else:
            data_info = ServiceUnit.objects.filter(userxu=1)
        print(data_info)
        for i in data_info.values('unit_name','id'):
            # print(j)
            print(i)
            dic = {}
            dic['label'] = i['unit_name']
            dic['value'] = i['id']
            # dic['label'] = i['id']
            re_data.append(dic)
        re_data_new={'data': re_data}
        return JsonResponse(re_data_new)

#创建单位与机器人中间表
class intermediate(View):
    def post(self,request,id):
        print(request.body,'1111111111111')
        data_info = request.body
        json_obj = json.loads(data_info)['data']
        print(data_info,"oooollllllllll")
        unit_name_id=json_obj['region']
        data_info = ServiceUnit.objects.filter(userxu=1)
        unit_name = ''
        for i in data_info.values('id', 'unit_name', 'unit_abb', 'use', 'phone', 'iphone', 'address', 'uintstate',
                                  'userxu'):
            if i['id'] == unit_name_id:
                unit_name = i['unit_name']
        print('单位名称：：：',unit_name)
        Intermediate.objects.filter(unit_name_id=unit_name_id).delete()
        for i in json_obj['type']:
            #i是机器人名称
            w=RobotInfo.objects.get(robot_name=i).id
            Intermediate.objects.create(unit_name_id=unit_name_id,robot_id=w)
        print(json_obj)
        log_inf.info('系统用户'+'admin'+'操作系统，服务单位绑定机器人'+str(json_obj['type']))
        return JsonResponse({'code': 1})

    def get(self,request,id):
        data_list=[]
        print(request,'00000000',id)
        if id != 0:
            data_info=Intermediate.objects.filter(unit_name_id=id)
            for i in data_info:
                robot_id = RobotInfo.objects.get(id=i.robot_id).robot_name
                data_list.append(robot_id)
            print('机器人信息：：：：',data_list)
            return JsonResponse({'code':1,'data':data_list})
        else:
            data_info=Intermediate.objects.all()
            for i in data_info:
                print('所有机器人绑定情况data_info----->>>',i.unit_name_id)
                unit_name_id = ServiceUnit.objects.get(id=i.unit_name_id).unit_name
                robot_id = RobotInfo.objects.get(id=i.robot_id).robot_name
                print('------>>>>>>',i.unit_name_id)
                dist_d = {}
                print(str(i.createtime)[:10])
                dist_d['unit_name_id']=unit_name_id
                dist_d['robot_id']=robot_id
                dist_d['data']=str(i.createtime)[:10]
                data_list.append(dist_d)
            print('机器人信息222',data_list)
            return JsonResponse({'code':1,'data':data_list})