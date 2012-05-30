# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib import admin
import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

    
urlpatterns = patterns('',
    url(r'^sharings/', include('sharings.urls'), name='sharings'),
    url(r'^anothehomepage/$', 'sharings.views.index', name='anothehomepage'),
    url(r'^newversion/$', 'sharings.views.new_version', name='newversion'),
#    url(r'^$', 'sharings.views.hotest_sharings', name='homepage'),
#    url(r'^$', redirect_to, {'url':'/sharings/hotest/'}, name='homepage'),
    url(r'^$', redirect_to, {'url':'/newversion/'}, name='homepage'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'sysdata.auth.login', name='login'),
    url(r'^login_ajax/$', 'sysdata.auth.login_ajax'),
    url(r'^logout/$', 'sysdata.auth.logout', name='logout'),
    url(r'^regist/$', 'sysdata.auth.regist', name='regist'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
