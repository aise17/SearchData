"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webInfo.views import engine_list, cliet_list, file_query_list, file_results_list
from webInfo.views import get_engine, get_client, get_file_query, get_file_result, superuser
from webInfo.views import delete_client, delete_engine, delete_filequery, delete_fileresult
from webInfo.views import  engine_detail, client_detail, filequery_detail, fileresult_detail
from webInfo.views import  edit_engine, edit_client, edit_filequery, grph_client


from django.conf import settings
from django.conf.urls.static import static


from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #-----------------------------------------------------------------------------------------------------------
    #urls lists views
    url(r'^engine/', engine_list, name = 'engine-list'),
    url(r'^client/', cliet_list, name = 'client-list'),
    url(r'^file_query/', file_query_list, name = 'file_query_list'),
    url(r'^file_result/', file_results_list, name = 'file_results_list'),
    #-----------------------------------------------------------------------------------------------------------
    #urls details viwes
    url(r'^engine_detail/(?P<pk>\d+)/$', engine_detail, name = 'engine_detail'),
    url(r'^client_detail/(?P<pk>\d+)/$', client_detail, name = 'client_detail'),
    url(r'^filequery_detail/(?P<pk>\d+)/$', filequery_detail, name = 'filequery_detail'),
    url(r'^fileresult_detail/(?P<pk>\d+)/$', fileresult_detail, name = 'fileresult_detail'),
    #-----------------------------------------------------------------------------------------------------------
    #urls forms
    url(r'^get_engine/', get_engine, name = 'get_engine'),
    url(r'^get_client/', get_client, name = 'get_client'),
    url(r'^get_file_query/', get_file_query, name = 'get_file_query'),
    url(r'^get_file_result/', get_file_result, name = 'get_file_result'),
    #-----------------------------------------------------------------------------------------------------------
    #url delet registers
    url(r'^delete_client/(?P<pk>\d+)/$', delete_client, name = 'delete_client'),
    url(r'^delete_engine/(?P<pk>\d+)/$', delete_engine, name = 'delete_engine'),
    url(r'^delete_filequery/(?P<pk>\d+)/$', delete_filequery, name = 'delete_filequery'),
    url(r'^delete_fileresult/(?P<pk>\d+)/$', delete_fileresult, name = 'delete_fileresult'),


    url(r'^edit_engine/(?P<pk>\d+)/$', edit_engine, name = 'edit_engine'),
    url(r'^edit_client/(?P<pk>\d+)/$', edit_client, name = 'edit_client'),
    url(r'^edit_filequery/(?P<pk>\d+)/$', edit_filequery, name = 'edit_filequery'),
    #----------------------------------------------------------------------------------------------------------------    
    #registro de usuarios
    url(r'^$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/client'}, name='logout'),
    url(r'^register/', superuser, name = 'superuser'),
    url(r'^grph_client/(?P<pk>\d+)/$', grph_client, name = 'grph_client'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)