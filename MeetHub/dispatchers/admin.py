'''
Created on 05/nov/2013

@author: michele
'''
from django.contrib import admin
from dispatchers.models import Dispatcher,DebugDispatcher, TestDispatcher

admin.site.register(Dispatcher)
admin.site.register(DebugDispatcher)
admin.site.register(TestDispatcher)
