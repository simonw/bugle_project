from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import re
import urllib

register = template.Library()

username_re = re.compile('@[0-9a-zA-Z]+')
hashtag_re = re.compile('(^|\s)(#\S+)')

@register.filter
def buglise(s):
    s = unicode(s)
    
    usernames = set(User.objects.values_list('username', flat=True))
    def replace_username(match):
        username = match.group(0)[1:]
        if username.lower() == 'all':
            return '<strong>@all</strong>'
        if username in usernames:
            return '<a href="/%s/">@%s</a>' % (username, username)
        else:
            return '@' + username
    
    s = username_re.sub(replace_username, s)

    s = hashtag_re.sub(
        lambda m: '%s<a href="/search/?q=%s">%s</a>' % (
            m.group(1),
            urllib.quote(m.group(2)), 
            m.group(2),
        ),
        s
    )
    return mark_safe(s)
    
