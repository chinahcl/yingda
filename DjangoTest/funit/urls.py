from .views import *
from rest_framework import routers
from django.urls import path,include
from . import views


# router = routers.DefaultRouter()
# router.register(r"", Uint,basename='key')

urlpatterns=[
    path('', views.Test.as_view()),
    path('/', views.Test.as_view()),
    path('/<int:id>', views.Test.as_view()),
    path('/zhengchang', views.fronzen_unit.as_view()),
    path('/zhengchang/<int:id>', views.fronzen_unit.as_view()),
    path('/dongjie', views.thaw_unit.as_view()),
    path('/dongjie/<int:id>', views.thaw_unit.as_view()),
    path('/unit_name/<int:id>', views.unit_name.as_view()),
    path('/intermediate/<int:id>', views.intermediate.as_view())
]
