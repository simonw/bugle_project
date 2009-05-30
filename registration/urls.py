from django.conf.urls.defaults import *

urlpatterns = patterns("registration.views",
    url(r'^register/$', "register", name="register"),
)
urlpatterns += patterns('django.contrib.auth.views',

    url(r'^password/reset/$', "password_reset", name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
         "password_reset_confirm", name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', "password_reset_complete", name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', "password_reset_done", name='auth_password_reset_done'),
)
