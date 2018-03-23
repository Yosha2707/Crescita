
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns= [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^add/', views.add, name='add'),
    url(r'^insert$', views.insert, name='insert'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^update/(?P<id>\d+)$', views.update, name='update'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^import_file$', views.import_file, name='import_file'),
     ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



