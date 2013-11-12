'''
Created on 05/nov/2013

@author: michele
'''
from django.contrib import admin
from sources.models import Source, DebugSource, TestSource

admin.site.register(Source)
admin.site.register(DebugSource)
admin.site.register(TestSource)
