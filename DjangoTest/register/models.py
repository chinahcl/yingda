# from django.db import models
#
# # Create your models here.
# class UserProfile(models.Model):
#
#     username = models.CharField(max_length=11, verbose_name='用户名', unique=True)
#     password = models.CharField(max_length=32)
#     ment = models.CharField(max_length=30, verbose_name='部门')
#     use_id = models.CharField(max_length=18, verbose_name='身份证', unique=True)
#     unit_phone = models.CharField(max_length=18, verbose_name='办公电话')
#     chu_name = models.CharField(max_length=18, verbose_name='处室名称')
#     use_iphone = models.CharField(max_length=11, verbose_name='手机号',unique=True)
#     use_address = models.CharField(max_length=32, verbose_name='办公地址')
#     use_unit = models.CharField(max_length=32, verbose_name='单位名称')
#     # phone = models.CharField(max_length=11, unique=True)
#     #刚注册的用户 需要在激活邮件内 激活后 方可使用用户功能
#     is_active = models.BooleanField(default=False, verbose_name='是否激活')
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)
#
#     class Meta:
#
#         db_table = 'user_user_profile_old'