# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('sharings.views',
    url(r'^add/$', 'add_sharing'),
    url(r'^(?P<sharing_id>\d+)/$', 'detail'),
    url(r'^medias/auto_save/$', 'medias_auto_save'),
    url(r'^(?P<sharing_id>\d+)/comment/post/$', 'add_comment'),
    url(r'^ajax_add_sharing/$', 'ajax_add_sharing'),
    url(r'^ajax_delete_mediafile/$','ajax_delete_mediafile'),
    url(r'^all/$', 'all_sharings'),
    url(r'^hotest/$', 'hotest_sharings', name='hotest'),
    url(r'^myfollow/$', 'myfollow_sharings'),
    url(r'^tag/(?P<tag_id>\d+)/sharings/$', 'tag_sharings'),    
    url(r'^(?P<sharing_id>\d+)/vote/(?P<vote_value>(1|-1))/$', 'vote'),    
    url(r'^(?P<sharing_id>\d+)/follow/$', 'follow'),   
    url( r'^load_more/$', 'load_more_sharings', name = 'demo_load_more' ), 
    url(r'^report/','report',name='report'),
    url(r'^keywords_analysis/','keywords_analysis',name='keywords_analysis'),
    url(r'^manafactuser/$', 'manafactuser'),
    url(r'^(?P<sharing_id>\d+)/comments/$', 'list_comments'),
    
   
)
          
