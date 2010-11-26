from django.conf import settings
from django.utils import simplejson
import urllib2

class FayeClient(object):
    def __init__(self, url=settings.FAYE_URL, fail_silently=True):
        self.url = url
        self.fail_silently = fail_silently
        
    def publish(self, channel, data):
        # TODO: handle errors
        req = urllib2.Request(self.url, simplejson.dumps([{
            'channel': channel,
            'data': data,
        }]), headers={
            'Content-Type': 'application/json'
        })
        try:
            urllib2.urlopen(req)
        except urllib2.URLError:
            if self.fail_silently:
                pass
            else:
                raise

