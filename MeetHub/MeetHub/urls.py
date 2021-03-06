from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MeetHub.views.home', name='home'),
    # url(r'^MeetHub/', include('MeetHub.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^hubs/', include('hubs.urls')),
    url(r'^dispatchers/', include('dispatchers.urls')),
    url(r'^sources/', include('sources.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^commissioni/', include('commissioni.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
