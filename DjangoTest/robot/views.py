import json
import os,shutil
import time
import _thread
import pandas as pd
from django.conf import settings
from django.http import JsonResponse, FileResponse, StreamingHttpResponse
from django.utils.http import urlquote
from urllib.parse import quote
from django.core.files.base import ContentFile
from DjangoTest.settings import MEDIA_ROOT, MEDIA_URL
from login.models import UserProfile
from .models import RobotInfo, Use_Robot_inter, fa_piao_cha_yan, fa_piao_shi_bie
from funit.models import Intermediate
from django.shortcuts import render
from .fa_piao_cha_yan import main_start
# Create your views here.
from django.views import View
from django.utils.encoding import escape_uri_path

import logging

log_err=logging.getLogger('err')
log_inf=logging.getLogger('inf')


#增加机器人及路径
#查询机器人
class robot_manage(View):
    def post(self, request,id):
        print(id)
        print('增加机器人及路径')
        data_info = request.body
        print(json.loads(data_info)['name'],type(json.loads(data_info)['name']),'机器人。。。。。')
        data_info = json.loads(data_info)['data']
        syx_name = json.loads(request.body)['name']
        print(data_info)
        if id == 0:
            robot_name=data_info['robot_name']
            robot_path=data_info['robot_path']
            try:
                rusult=RobotInfo.objects.create(robot_name=robot_name,robot_path=robot_path)
                print('机器人增加成功')
                log_inf.info('系统用户'+syx_name+'操作系统，机器人：'+robot_name +'增加成功，机器人路径为：'+robot_path)
                return JsonResponse({'code': 1})
            except Exception as e:
                log_err.info('系统用户'+syx_name+'操作系统，机器人：'+robot_name+'添加失败，账号重复！')
                return JsonResponse({'code': 0})
        else:
            data_info_w = RobotInfo.objects.get(id=id)
            try:
                print(id)
                # data_info_w = RobotInfo.objects.get(id=id)
                old_robotname = data_info_w.robot_name
                data_info_w.robot_name = data_info['robot_name']
                data_info_w.robot_path = data_info['robot_path']
                data_info_w.save()
                log_inf.info('系统用户'+syx_name+'操作系统，机器人：'+old_robotname+'信息修改为'+str(data_info))
                return JsonResponse({'code': 1,'data': {'id':id, 'robot_name':data_info_w.robot_name, 'robot_path':data_info_w.robot_path}})
            except Exception as e:
                print('机器人信息修改3')
                log_err.error('系统用户'+syx_name+'操作系统，机器人：' + data_info_w.robot_name + '信息修改失败')
                return JsonResponse({'code': 2})

    def get(self, request,id):
        print('查询机器人')
        print(id)
        re_data = []
        if id != 0:
            data_info = RobotInfo.objects.filter(id=id)
        else:
            data_info = RobotInfo.objects.filter(is_active=0)
            # data_info = RobotInfo.objects.all()
        print(data_info,"+++++++++++++++")
        for i in data_info.values('robot_name','robot_path','is_active','id'):
            # print(j)
            print(i)
            dic = {}
            dic['robot_name'] = i['robot_name']
            dic['robot_path'] = i['robot_path']
            dic['is_active'] = i['is_active']
            dic['id'] = i['id']
            re_data.append(dic)
        re_data_new={'data': re_data}
        return JsonResponse(re_data_new)


#变更状态为冻结
class robot_manage_dongjie(View):
    def post(self, request,id):
        data_infos = RobotInfo.objects.filter(is_active=0)
        robot_name = ''
        for i in data_infos.values('robot_name', 'robot_path', 'is_active', 'id'):
            if i['id'] == id:
                robot_name = i['robot_name']
        data_info=request.body
        data_info=json.loads(data_info)['data']
        syx_name=json.loads(request.body)['name']
        data_info_d=RobotInfo.objects.get(id=id)
        print(data_info)
        data_info_d.is_active=data_info
        data_info_d.save()
        log_inf.info('系统用户'+syx_name+'操作系统，机器人：'+robot_name+'状态变更为冻结！')
        return JsonResponse({'code': 1})

    def get(self, request,id):
        print(request,'变更状态为冻结1')
        print(id,'id=')
        re_data = []
        if id != 0:
            data_info = RobotInfo.objects.filter(is_active=0,id=id)
        else:
            data_info = RobotInfo.objects.filter(is_active=0)
        print(data_info,'@@@@=====')
        for i in data_info.values('robot_name','robot_path','is_active','id'):
            # print(j)
            print(i)
            dic = {}
            dic['robot_name'] = i['robot_name']
            dic['robot_path'] = i['robot_path']
            dic['is_active'] = i['is_active']
            dic['id'] = i['id']
            re_data.append(dic)
        re_data_new={'data': re_data}
        return JsonResponse(re_data_new)

#变更状态为解冻
class robot_manage_jiedong(View):
    def post(self, request,id):
        print('变更状态为解冻',id)
        data_infos = RobotInfo.objects.filter(is_active=1)
        robot_name = ''
        for i in data_infos.values('robot_name','robot_path','is_active','id'):
            if i['id'] == id:
                robot_name = i['robot_name']
        data_info=request.body
        data_info=json.loads(data_info)['data']
        syx_name=json.loads(request.body)['name']
        print(data_info)
        data_info_d=RobotInfo.objects.get(id=id)
        print(data_info)
        data_info_d.is_active=data_info
        data_info_d.save()
        log_inf.info('系统用户'+syx_name+'操作系统，机器人：'+robot_name+'解冻成功！')
        return JsonResponse({'code': 1})

    def get(self, request,id):
        print('变更状态为解冻')
        print(id)
        re_data = []
        if id != 0:
            data_info = RobotInfo.objects.filter(is_active=1,id=id)
        else:
            data_info = RobotInfo.objects.filter(is_active=1)
        print(data_info)
        for i in data_info.values('robot_name','robot_path','is_active','id'):
            # print(j)
            print(i)
            dic = {}
            dic['robot_name'] = i['robot_name']
            dic['robot_path'] = i['robot_path']
            dic['is_active'] = i['is_active']
            dic['id'] = i['id']
            re_data.append(dic)
        re_data_new={'data': re_data}
        return JsonResponse(re_data_new)


#获取单位绑定的机器人
def get_unit_id(request,id):
    re_data=[]
    print('获取单位绑定的机器人',id)
    data_info = Intermediate.objects.filter(unit_name_id=id)
    # data_info = Intermediate.objects.all()
    print(data_info)
    for i in data_info.values('robot_id'):
        # print(i)
        robot_id = RobotInfo.objects.get(id=i['robot_id']).robot_name
        # print(robot_id)
        re_data.append(robot_id)
    print('re_data::',re_data)
    return JsonResponse({'data':re_data})

#创建用户和机器人绑定关系
class use_in_robot(View):
    def post(self, request,name):
        print(name,'创建用户和机器人绑定关系')
        data_info=request.body
        syx_name = json.loads(data_info)['name']
        data_info=json.loads(data_info)['data']
        # print(data_info)
        user_name=data_info['username']
        robot_name=data_info['type']
        print(user_name,robot_name)
        log_inf.info("系统用户："+syx_name+"操作系统，用户“"+user_name+"”绑定机器人，机器人名称为："+str(robot_name).replace("[","").replace("]",""))
        u_id=UserProfile.objects.get(username=user_name).id
        Use_Robot_inter.objects.filter(u_id=u_id).delete()
        for i in robot_name:
            robot_id=RobotInfo.objects.get(robot_name=i).id
            Use_Robot_inter.objects.create(u_id=u_id,robot_id=robot_id)
        return JsonResponse({'code':1})

    def get(self,request,name):
        re_datas=[]
        print('name------>>>>>',name)
        # data_info=request.body
        # data_info=json.loads(data_info)['data']
        # user_name = data_info['username']
        u_id = UserProfile.objects.get(username=name).id
        # print('name-------->>>>>',name)
        use_data=Use_Robot_inter.objects.filter(u_id=u_id)
        for i in use_data.values('robot_id'):
            print('i',i['robot_id'])
            robot_name = RobotInfo.objects.get(id=i['robot_id']).robot_name
            re_datas.append(robot_name)
        return JsonResponse({'code':1, 'data':re_datas})

#获取机器人列表
class use_get_robot_list(View):
    def get(self,request,name):
        re_data=[]
        print('name',name[1:-2])
        name1=name.replace('"','')
        u_id = UserProfile.objects.get(username=name1).id
        print(u_id)
        data_info=Use_Robot_inter.objects.filter(u_id=u_id)
        for i in data_info.values('robot_id'):
            dict_data={}
            print(i['robot_id'])
            robot_info=RobotInfo.objects.get(id=i['robot_id'])
            dict_data['name']=robot_info.robot_name
            dict_data['url'] = robot_info.robot_path
            dict_data['uindex']=robot_info.robot_path.split('/')[2]
            re_data.append(dict_data)
        print(re_data,'++++++++++++++++++')
        return JsonResponse({'code':1, 'data':re_data,'user_name':name})
        # print(name1)

#发票查验机器人
class fa_piao_cha_yan_view(View):

    def get(self,request,name):
        print(request)
        list_data=[]
        data_info=fa_piao_cha_yan.objects.filter(name=name)
        print(data_info.values('name','file','created_time'))
        for i in data_info.values('id','name','file','created_time','file_state','down_file'):
            dict_data= {}
            w_name=i['file'].split('/')[-1]
            print(w_name)
            created_time=i['created_time'].strftime('%Y-%m-%d %H:%M:%S')
            dict_data['w_name']=w_name
            dict_data['file_state']=i['file_state']
            dict_data['down_file']=i['down_file']
            dict_data['id']=i['id']
            dict_data['name']=i['name']
            dict_data['file']=i['file']
            dict_data['created_time']=created_time
            list_data.append(dict_data)
        return JsonResponse({'code':1, 'data':list_data})

    def post(self,request,name):
        file=request.FILES.get('file')
        name=request.POST.get('name')
        fa_piao_cha_yan.objects.create(file=file,name=name)
        return JsonResponse({'code':1})

#发票查验启动
class fa_piao_cha_yan_view_start(View):
    def get(self,request,id):
        change_info = fa_piao_cha_yan.objects.get(id=id)

        def file_iterator(file_name, chunk_size=512):  # 用于形成二进制数据
            with open(file_name, "rb") as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        filepath = settings.MEDIA_ROOT.replace('/', '\\')+str(change_info.down_file).replace('/', '\\')
        print('filepath________',filepath)
        ff = filepath.split('\\')[-1]
        response = StreamingHttpResponse(file_iterator(filepath))
        response['Content-Type'] = 'application/octet-stream'
        response['Access-Control-Expose-Headers'] = "Content-Disposition, Content-Type"
        response['Content-Disposition'] = 'attachment; {}'.format("filename*=utf-8''{}".format(quote(ff)))

        return response


    def post(self,request,id):
        print('发票查验机器人启动')
        data_info = request.body
        data_info = json.loads(data_info)['data']
        print(data_info)
        #变更状态
        change_info = fa_piao_cha_yan.objects.get(id=id)
        print('change_info.file----->>>>',change_info.file)
        change_info.file_state = '2'
        change_info.save()
        path1 = os.getcwd()
        #文件绝对路径
        path = path1 + '\\upload\\'+str(change_info.file).replace('/','\\')
        #上一层路径
        new_paht = '\\'.join(path.split('\\')[:-1])
        #文件名
        new_paht_1 = path.split('\\')[-1].split('.')[0]
        print('new_paht', new_paht)
        # 创建文件
        create_file=new_paht + '\\'+str(new_paht_1)
        os.makedirs(create_file)
        # os.makedirs(new_paht + '\\' + str(new_paht_1)+'\\点击查验后图片')
        # os.makedirs(new_paht + '\\' + str(new_paht_1)+'\\验证码图片')
        shutil.copy(path,new_paht+'\\'+str(new_paht_1))
        # print(data_i)
        #启动机器人 参数：path
        _thread.start_new_thread(main_start,(id,create_file))
        # print('机器人运行结束')
        # time.sleep(10)
        # change_info.file_state = '3'
        # change_info.save()
        return JsonResponse({'code': 1})


class fa_piao_shi_bie_view(View):
    def get(self,request,name):
        list_data=[]
        if name == 'admin':
            data_info = fa_piao_shi_bie.objects.all()
        else:
            data_info=fa_piao_shi_bie.objects.filter(name=name)
        print(data_info.values('name','file','created_time'))
        for i in data_info.values('id','name','file','created_time','file_state','down_file'):
            dict_data= {}
            w_name=i['file'].split('/')[-1]
            print(w_name)
            created_time=i['created_time'].strftime('%Y-%m-%d %H:%M:%S')
            dict_data['w_name']=w_name
            dict_data['file_state']=i['file_state']
            dict_data['down_file']=i['down_file']
            dict_data['id']=i['id']
            dict_data['name']=i['name']
            dict_data['file']='http://'+request.get_host()+MEDIA_URL+i['file']
            dict_data['created_time']=created_time
            list_data.append(dict_data)
        return JsonResponse({'code':1, 'data':list_data})

    def post(self,request,name):
        file=request.FILES.get('file')
        name=request.POST.get('name')
        fa_piao_shi_bie.objects.create(file=file,name=name)
        return JsonResponse({'code':1})


class fa_piao_shi_bie_view_start(View):
    def get(self,request,id):
        change_info = fa_piao_shi_bie.objects.get(id=id)

        def file_iterator(file_name, chunk_size=512):  # 用于形成二进制数据
            with open(file_name, "rb") as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
        filepath = settings.MEDIA_ROOT.replace('/', '\\')+str(change_info.down_file).replace('/', '\\')
        print('filepath________',filepath)
        ff = filepath.split('\\')[-1]
        response = StreamingHttpResponse(file_iterator(filepath))
        response['Content-Type'] = 'application/octet-stream'
        response['Access-Control-Expose-Headers'] = "Content-Disposition, Content-Type"
        response['Content-Disposition'] = 'attachment; {}'.format("filename*=utf-8''{}".format(quote(ff)))
        return response


    def post(self,request,id):
        import base64
        print('启动机器人')
        data_info = request.body
        data_name=request.POST.get('name')
        data_=request.POST.get('file')
        change_info = fa_piao_shi_bie.objects.get(id=id)
        name_list=str(change_info.file).split('/')[:-1]
        name_str='/'.join(name_list)
        file_path=os.path.join(MEDIA_ROOT,data_name)
        file_path=os.path.join(MEDIA_ROOT,name_str+'/'+data_name)
        with open(file_path,'wb') as f:
            f.write(base64.b64decode(data_))
            # f.write(data_.encode(encoding='utf-8'))
            # f.write(data_.decode('utf-8'))
        change_info.down_file=name_str+'/'+data_name
        change_info.file_state='2'
        change_info.save()
        #变更状态
        '''
        change_info = fa_piao_shi_bie.objects.get(id=id)
        print('change_info.file----->>>>',change_info.file)
        change_info.file_state = '2'
        change_info.save()
        path1 = os.getcwd()
        #文件绝对路径
        path = path1 + '\\upload\\'+str(change_info.file).replace('/','\\')
        #上一层路径
        new_paht = '\\'.join(path.split('\\')[:-1])
        #文件名
        new_paht_1 = path.split('\\')[-1].split('.')[0]
        print('new_paht', new_paht)
        # 创建文件
        create_file=new_paht + '\\'+str(new_paht_1)
        os.makedirs(create_file)
        # os.makedirs(new_paht + '\\' + str(new_paht_1)+'\\点击查验后图片')
        # os.makedirs(new_paht + '\\' + str(new_paht_1)+'\\验证码图片')
        shutil.copy(path,new_paht+'\\'+str(new_paht_1))
        # print(data_i)
        #启动机器人 参数：path
        # _thread.start_new_thread(main_start,(id,create_file))
        # print('机器人运行结束')
        # time.sleep(10)
        # change_info.file_state = '3'
        # change_info.save()
        '''
        return JsonResponse({'code': 1})