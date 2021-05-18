# Generated by Django 3.0.7 on 2021-03-23 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Intermediate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name_id', models.CharField(max_length=50, verbose_name='单位id编号')),
                ('robot_id', models.CharField(max_length=50, verbose_name='机器人id编号')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'intermediate_unit_robot',
            },
        ),
        migrations.CreateModel(
            name='ServiceUnit',
            fields=[
                ('id', models.IntegerField(auto_created=True, editable=False, primary_key=True, serialize=False)),
                ('unit_name', models.CharField(max_length=50, unique=True, verbose_name='单位名称')),
                ('unit_abb', models.CharField(max_length=30, verbose_name='单位简称')),
                ('use', models.CharField(max_length=30, verbose_name='联系人')),
                ('phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('iphone', models.CharField(max_length=11, verbose_name='手机号')),
                ('address', models.CharField(max_length=50, verbose_name='办公地址')),
                ('uintstate', models.IntegerField(verbose_name='状态')),
                ('userxu', models.CharField(max_length=50, verbose_name='公司序号')),
                ('createtime', models.DateTimeField(auto_now_add=True)),
                ('updatedtime', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'service_unit',
            },
        ),
    ]