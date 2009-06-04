from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'bugle.views.homepage'),
    (r'^all/$', 'bugle.views.all'),
    (r'^toggle/$', 'bugle.views.toggle'),
    (r'^favourite/$', 'bugle.views.favourite'),
    (r'^stats/$', 'bugle.views.stats'),
    (r'^favourites/$', 'bugle.views.all_favourites'),
    (r'^mentions/$', 'bugle.views.all_mentions'),
    (r'^pastes/$', 'bugle.views.all_pastes'),
    (r'^todos/$', 'bugle.views.all_todos'),
    (r'^blast/(\d+)/$', 'bugle.views.blast'),
    #(r'^autorefresh/$', 'bugle.views.homepage', {'autorefresh': True}),
    #(r'^autorefresh/since/$', 'bugle.views.since'),
    (r'^post/$', 'bugle.views.post'),
    (r'^post/api/$', 'bugle.views.post_api'),
    (r'^delete/$', 'bugle.views.delete'),
    (r'^account/', include('registration.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.OUR_ROOT, 'static')
    }),
    
    (r'^([a-zA-Z0-9]+)/$', 'bugle.views.profile'),
    (r'^([a-zA-Z0-9]+)/favourites/$', 'bugle.views.favourites'),
    (r'^([a-zA-Z0-9]+)/mentions/$', 'bugle.views.mentions'),
    (r'^([a-zA-Z0-9]+)/pastes/$', 'bugle.views.pastes'),
    (r'^([a-zA-Z0-9]+)/todos/$', 'bugle.views.todos'),

)
