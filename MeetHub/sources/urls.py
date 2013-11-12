'''
Created on 06/nov/2013

@author: michele
'''
from django.conf.urls import patterns, url

from sources import views, models

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^debug/$', views.DebugIndexView.as_view(), 
        name=models.DebugSource.get_index_url_name()),
    url(r'^debug/(?P<pk>\d+)/$', views.DebugSourceView.as_view(), 
        name=models.DebugSource.get_detail_url_name()),
    url(r'^test/$', views.TestIndexView.as_view(), 
        name=models.TestSource.get_index_url_name()),
    url(r'^test/(?P<pk>\d+)/$', views.TestSourceView.as_view(), 
        name=models.TestSource.get_detail_url_name()),
)