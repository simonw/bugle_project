from django.db import models
import md5

class Blast(models.Model):
    user = models.ForeignKey('auth.User', related_name = 'blasts')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    
    def colour(self):
        return md5.new(str(self.user)).hexdigest()[:6]
    
    def __unicode__(self):
        return u'%s at %s' % (self.user, self.created)
    