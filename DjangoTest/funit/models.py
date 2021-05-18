from django.db import models
from rest_framework import serializers

# Create your models here.

#创建服务单位信息数据库

class ServiceUnit(models.Model):
    id = models.IntegerField(primary_key=True, editable=False,auto_created=True)
    unit_name = models.CharField(max_length=50,verbose_name='单位名称',unique=True)
    unit_abb = models.CharField(max_length=30,verbose_name='单位简称')
    use = models.CharField(max_length=30,verbose_name='联系人')
    phone = models.CharField(max_length=11,verbose_name='联系电话')
    # iphone = models.CharField(max_length=11,verbose_name='手机号',unique=True)
    iphone = models.CharField(max_length=11,verbose_name='手机号')
    address = models.CharField(max_length=50,verbose_name='办公地址')
    uintstate = models.IntegerField(verbose_name='状态')
    userxu = models.CharField(max_length=50,verbose_name='公司序号')
    createtime = models.DateTimeField(auto_now_add=True)
    updatedtime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_unit'

#序列化
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceUnit
        fields = '__all__'

class Intermediate(models.Model):
    unit_name_id=models.CharField(max_length=50,verbose_name='单位id编号')
    robot_id=models.CharField(max_length=50,verbose_name='机器人id编号')
    createtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'intermediate_unit_robot'