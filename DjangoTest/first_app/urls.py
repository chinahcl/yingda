from django.urls import path

from . import views

urlpatterns=[
    path('',views.one_web,name='index')
]