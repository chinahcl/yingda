from django.urls import path

from . import views

urlpatterns=[
    path('/<int:id>', views.robot_manage.as_view()),
    path('/dongjie/<int:id>', views.robot_manage_dongjie.as_view()),
    path('/jiedong/<int:id>', views.robot_manage_jiedong.as_view()),
    path('/unit_id/<int:id>',views.get_unit_id),
    path('/use_in_robot/<str:name>',views.use_in_robot.as_view()),
    path('/use_get_robot_list/<str:name>',views.use_get_robot_list.as_view()),
    path('/fa_piao_cha_yan/<str:name>',views.fa_piao_cha_yan_view.as_view()),
    path('/fa_piao_cha_yan_start/<int:id>',views.fa_piao_cha_yan_view_start.as_view()),
    path('/fa_piao_shi_bie/<str:name>',views.fa_piao_shi_bie_view.as_view()),
    path('/fa_piao_shi_bie_start/<int:id>',views.fa_piao_shi_bie_view_start.as_view())
]