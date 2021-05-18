from django.db import models
from rest_framework import serializers
# Create your models here.
# from django.db import models
#
# # Create your models here.
class RobotInfo(models.Model):
    robot_name = models.CharField(max_length=11, verbose_name='机器人名称', unique=True)
    robot_path=models.CharField(max_length=50,verbose_name='机器人路径')
    #刚注册的用户 需要在激活邮件内 激活后 方可使用用户功能
    is_active = models.BooleanField(max_length=10,default=0, verbose_name='是否激活')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:

        db_table = 'robot_data_info'


class Use_Robot_inter(models.Model):
    u_id=models.CharField(max_length=50,verbose_name='用户id编号')
    robot_id=models.CharField(max_length=50,verbose_name='机器人id编号')
    createtime = models.DateTimeField(auto_now_add=True)

    class Meta:

        db_table = 'intermediate_use_robot'


class fa_piao_cha_yan(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='fa_piao_cha_yan/%Y/%m/%d/')
    file_state = models.CharField(max_length=10,default=1)
    down_file = models.FileField(upload_to='fa_piao_cha_yan/%Y/%m/%d/')
    created_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'fa_piao_cha_yan_table'

class fa_piao_shi_bie(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='fa_piao_shi_bie/%Y/%m/%d/')
    file_state = models.CharField(max_length=10,default=1)
    down_file = models.FileField(upload_to='fa_piao_shi_bie/%Y/%m/%d/')
    created_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'fa_piao_cha_shi_bie'
# #上传下载序列化
# class FileSerializer(serializers.ModelSerializer):
#     created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
#     class Meta:
#         model = fa_piao_cha_yan
#         fields = '__all__'