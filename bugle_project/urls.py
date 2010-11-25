from twitter_api import views
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
    (r'^files/$', 'bugle.views.all_files'),
    (r'^todos/$', 'bugle.views.all_todos'),
    (r'^search/$', 'bugle.views.search'),
    (r'^blast/(\d+)/$', 'bugle.views.blast'),
    #(r'^autorefresh/$', 'bugle.views.homepage', {'autorefresh': True}),
    #(r'^autorefresh/since/$', 'bugle.views.since'),
    (r'^post/$', 'bugle.views.post'),
    (r'^post/api/$', 'bugle.views.post_api'),
    (r'^post_image/$', 'bugle.views.post_image'),
    (r'^delete/$', 'bugle.views.delete'),
    (r'^account/', include('registration.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    
    # Twitter API
    (r'^(?:1/)?statuses/public_timeline\.(?P<format>json|xml)', views.TimelineView()),
    (r'^(?:1/)?statuses/(?:home|friends)_timeline\.(?P<format>json|xml)', views.LoginRequiredTimelineView()),
    (r'^(?:1/)?statuses/user_timeline\.(?P<format>json|xml)', views.UserTimelineView()),
    (r'^(?:1/)?statuses/(?:mentions|replies)\.(?P<format>json|xml)', views.MentionsView()),
    (r'^(?:1/)?statuses/update\.(?P<format>json|xml)', views.StatusUpdateView()),
    (r'^(?:1/)?users/show\.(?P<format>json|xml)', views.UsersShowView()),
    (r'^(?:1/)?search\.(?P<format>json|xml)', views.SearchView()),
    (r'^(?:1/)?favorites/create/(?P<id>.+?)\.(?P<format>json|xml)', views.FavoritesCreateView()),
    (r'^(?:1/)?favorites/destroy/(?P<id>.+?)\.(?P<format>json|xml)', views.FavoritesDestroyView()),
    (r'^(?:1/)?favorites(?:/(?P<id>.+?))?\.(?P<format>json|xml)', views.FavoritesView()),
    (r'^(?:1/)?account/verify_credentials\.(?P<format>json|xml)', views.VerifyCredentialsView()),
    (r'^(?:1/)?account/rate_limit_status\.(?P<format>json|xml)', views.RateLimitStatusView()),
    (r'^(?:1/)?trends/current\.(?P<format>json|xml)', views.CurrentTrendsView()),
    (r'^(?:1/)?oauth/access_token', 'twitter_api.views.oauth_access_token'),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.OUR_ROOT, 'static')
    }),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.OUR_ROOT, 'uploads')
    }),
    
    url(r'^([a-zA-Z0-9]+)/$', 'bugle.views.profile', name='profile'),
    (r'^([a-zA-Z0-9]+)/favourites/$', 'bugle.views.favourites'),
    (r'^([a-zA-Z0-9]+)/mentions/$', 'bugle.views.mentions'),
    (r'^([a-zA-Z0-9]+)/pastes/$', 'bugle.views.pastes'),
    (r'^([a-zA-Z0-9]+)/files/$', 'bugle.views.files'),
    (r'^([a-zA-Z0-9]+)/todos/$', 'bugle.views.todos'),

)
