from django.contrib.auth.models import User
import re

class GhettoOAuthMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user_id = self._get_token_from_header(request, 'HTTP_AUTHORIZATION')
        if not user_id:
            user_id = self._get_token_from_header(request, 'HTTP_X_VERIFY_CREDENTIALS_AUTHORIZATION')

        if 'oauth_token' in request.GET:
            user_id = request.GET['oauth_token']
        if user_id:
            request.user = User.objects.get(pk=user_id)
        return view_func(request, *view_args, **view_kwargs)
    
    def _get_token_from_header(self, request, header):
        if header in request.META and request.META[header].startswith('OAuth'):
            m = re.search(r'oauth_token="(\d+)"', request.META[header])
            if m:
                return m.group(1)

