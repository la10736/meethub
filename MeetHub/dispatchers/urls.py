'''
Created on 06/nov/2013

@author: michele
'''
from django.conf.urls import patterns, url

from dispatchers import views, models

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='disptachers.index'),
    url(r'^debug/$', views.DebugIndexView.as_view(), 
        name=models.DebugDispatcher.get_index_url_name()),
    url(r'^debug/(?P<pk>\d+)/$', views.DebugDispatcherView.as_view(), 
        name=models.DebugDispatcher.get_detail_url_name()),
    url(r'^test/$', views.TestIndexView.as_view(), 
        name=models.TestDispatcher.get_index_url_name()),
    url(r'^test/(?P<pk>\d+)/$', views.TestDispatcherView.as_view(), 
        name=models.TestDispatcher.get_detail_url_name()),
)