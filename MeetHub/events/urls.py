'''
Created on 06/nov/2013

@author: michele
'''
from django.conf.urls import patterns, url

from events import models, views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='events.index'),
    url(r'^(?P<pk>\d+)/$', views.EventView.as_view(), 
        name=models.Event.get_detail_url_name()),
)