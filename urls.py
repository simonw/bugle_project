from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'bugle.views.homepage'),
    (r'^post/$', 'bugle.views.post'),
    (r'^account/', include('registration.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    
    (r'^admin/', include(admin.site.urls)),
)
