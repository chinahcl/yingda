from django.db import models
from rest_framework import serializers


# Create your models here.
class FileModel(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='upload/')
    created_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'upload'


#上传下载序列化
class FileSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = FileModel
        fields = '__all__'