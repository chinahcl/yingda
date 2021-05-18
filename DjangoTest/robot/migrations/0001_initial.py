# Generated by Django 3.0.7 on 2021-03-23 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RobotInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('robot_name', models.CharField(max_length=11, unique=True, verbose_name='机器人名称')),
                ('robot_path', models.CharField(max_length=50, verbose_name='机器人路径')),
                ('is_active', models.BooleanField(default=0, max_length=10, verbose_name='是否激活')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'robot_data_info',
            },
        ),
    ]