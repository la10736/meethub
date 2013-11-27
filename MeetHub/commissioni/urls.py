'''
Created on 06/nov/2013

@author: michele
'''
from django.conf.urls import patterns, url

from commissioni import views

urlpatterns = patterns('',
    url(r'^$', views.CdZIndexView.as_view(), name='consigli.index'),
    url(r'^CdZ/(?P<pk>\d+)/$', views.CdZView.as_view(), 
        name='consigli.cdz'),
        
)