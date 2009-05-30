from django.db import models

class Blast(models.Model):
    user = models.ForeignKey('auth.User')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return u'%s at %s' % (self.user, self.created)
    