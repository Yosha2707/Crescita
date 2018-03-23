from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.index, name='index'),
    url(r'^profit_master$', views.index, name='index'),
    ]
