from django import template
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import re

register = template.Library()

username_re = re.compile('@[0-9a-zA-Z]+')

@register.filter
def buglise(s):
    s = unicode(s)
    def replace_username(match):
        username = match.group(0)[1:]
        try:
            u = User.objects.get(username = username)
        except User.DoesNotExist:
            return '@' + username
        return '<a href="/%s/">@%s</a>' % (username, username)
    
    return mark_safe(username_re.sub(replace_username, s))
