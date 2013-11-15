'''
Created on 06/nov/2013

@author: michele
'''
from django.conf.urls import patterns, url

from hubs import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='hubs.index'),
    url(r'^panel/(?P<pk>\d+)/$', views.HubDispatchPanel.as_view(), 
        name='hubs.hubpanel'),
        
)