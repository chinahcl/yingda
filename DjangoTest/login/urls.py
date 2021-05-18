from django.urls import path

from . import views

urlpatterns=[
    path('',views.users,name='index'),
    path('tubiao',views.reight.as_view(),name='tubiao'),
    path('tubiao/zhanshi',views.reight.as_view()),
    path('reight',views.reight.as_view(),name='regiht'),
    path('reight/query_use/<int:id>',views.reight.as_view()),
    # path('reight/zhengchang',views.zhengchang.as_view()),
    path('reight/zhengchang',views.zhengchang.as_view()),
    path('reight/zhengchang/<int:id>',views.zhengchang.as_view()),
    path('reight/<int:id>',views.reight_id.as_view()),
    # path('reight/dongjie', views.thaw_unit.as_view()),
    path('reight/dongjie', views.thaw_unit.as_view()),
    path('reight/dongjie/<int:id>', views.thaw_unit.as_view())
]