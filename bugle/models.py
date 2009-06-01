from django.db import models
import md5

class Blast(models.Model):
    user = models.ForeignKey('auth.User', related_name = 'blasts')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    extended = models.TextField(blank = True, null = True)
    
    def first_on_day(self):
        on_same_day = Blast.objects.filter(
            created__day = self.created.day,
            created__month = self.created.month,
            created__year = self.created.year,
        )
        return on_same_day.filter(created__lt = self.created).count() == 0
    
    class Meta:
        ordering = ('-created',)
    
    def colour(self):
        return md5.new(str(self.user)).hexdigest()[:6]
    
    def __unicode__(self):
        return u'%s at %s' % (self.user, self.created)
    