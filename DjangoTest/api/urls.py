from django.urls import path

from . import views

urlpatterns=[
    path('findUserName',views.findUserName,name='index'),
    path('register',views.register,name='index'),
    path('login',views.login,name='index'),
    path('all_info',views.all_info,name='all_info'),
    path('single_add_unit',views.single_add_unit,name='all_info')
]