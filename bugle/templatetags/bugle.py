from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import re

register = template.Library()

username_re = re.compile('@[0-9a-zA-Z]+')

@register.filter
def buglise(s):
    s = unicode(s)
    if not username_re.match(s):
        return mark_safe(s)
    
    usernames = set(User.objects.values_list('username', flat=True))
    def replace_username(match):
        username = match.group(0)[1:]
        if username.lower() == 'all':
            return '<strong>@all</strong>'
        if username in usernames:
            return '<a href="/%s/">@%s</a>' % (username, username)
        else:
            return '@' + username
    
    return mark_safe(username_re.sub(replace_username, s))
