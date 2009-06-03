from django.db import models
from django.utils.safestring import mark_safe
import md5, re

todo_re = re.compile('^todo:?\s+', re.I)

class Blast(models.Model):
    user = models.ForeignKey('auth.User', related_name = 'blasts')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    extended = models.TextField(blank = True, null = True)
    done = models.BooleanField(default = False)
    mentioned_users = models.ManyToManyField(
        'auth.User', related_name='mentions'
    )
    
    def checkbox(self):
        return mark_safe(
        '''<form action="/toggle/" method="POST" class="donebox">
        <div>
            <input type="image" src="/static/img/%(img)s.png"
                name="%(verb)s-%(pk)s" alt="%(img)s">
            </div>
        </form>
        ''' % {
            'img': self.done and 'checked' or 'unchecked',
            'pk': self.pk,
            'verb': self.done and 'uncheck' or 'check',
        })
    
    def is_todo(self):
        return todo_re.match(self.message)
    
    def message_without_todo(self):
        return todo_re.sub('', self.message)
    
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
    