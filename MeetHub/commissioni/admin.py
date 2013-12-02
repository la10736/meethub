'''
Created on 05/nov/2013

@author: michele
'''
from django.contrib import admin
from commissioni.models import CdZ, Commissione

admin.site.register(Commissione)
admin.site.register(CdZ)