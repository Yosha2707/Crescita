"""
Definition of urls for crescita_vs.
"""


from datetime import datetime
from venv import create
from app import views
import mode_master
import raw_packing_master
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views

import app.forms
import app.views
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
     url(r'^mode_master/', include('mode_master.urls')),
     url(r'^raw_packing_master/', include('raw_packing_master.urls')),
     url(r'^manufacturing_cost_master/', include('manufacturing_cost_master.urls')),
     url(r'^import$', app.views.import_profit, name='import_profit'),
     url(r'^export$', app.views.export, name='export'),
     url(r'^cost_price/', include('cost_price.urls')),
     url(r'^users/', app.views.users, name='users'),
     url(r'^profit_master/', app.views.profit_master, name='profit_master'),
     url(r'^add/', app.views.add, name='add'),
     url(r'^create/', app.views.create, name='create'),
     url(r'^import-test$', app.views.import_file, name='import_test'),
     
     ]
    
