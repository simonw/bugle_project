from django.contrib.auth.models import User
import re

class GhettoOAuthMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user_id = None
        if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION'].startswith('OAuth'):
            m = re.search(r'oauth_token="(\d+)"', 
                    request.META['HTTP_AUTHORIZATION'])
            if m:
                user_id = m.group(1)
        if 'oauth_token' in request.GET:
            user_id = request.GET['oauth_token']
        if user_id:
            request.user = User.objects.get(pk=user_id)
        return view_func(request, *view_args, **view_kwargs)
