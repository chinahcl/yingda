# Generated by Django 3.0.7 on 2021-03-12 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='upload/')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'upload',
            },
        ),
    ]
