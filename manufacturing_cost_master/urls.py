
from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.my_custom_sql, name='my_custom_sql'),
    url(r'^add$', views.add, name='add'),
    url(r'^my_custom_sql/', views.my_custom_sql, name='my_custom_sql'),
    url(r'^api/get_drugs/', views.get_places, name='get_places'),
    url(r'^api/get_drug/', views.get_place, name='get_place'),
    url(r'^insert$', views.insert, name='insert'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^edit/remove/(?P<id>\d+)$', views.remove, name='remove'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^import_file$', views.import_file, name='import_file'),

    ]

