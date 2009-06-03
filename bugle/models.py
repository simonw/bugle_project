from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import md5, re

todo_re = re.compile('^todo:?\s+', re.I)
username_re = re.compile('@[0-9a-zA-Z]+')

class Blast(models.Model):
    user = models.ForeignKey(User, related_name = 'blasts')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    extended = models.TextField(blank = True, null = True)
    is_todo = models.BooleanField(default = False)
    done = models.BooleanField(default = False)
    mentioned_users = models.ManyToManyField(User, related_name='mentions')
    favourited_by = models.ManyToManyField(User, related_name='favourites')
    
    def derive_mentioned_users(self, message=None):
        "Figure out mentioned users just from the message text"
        if message is None:
            message = self.message
        usernames = [
            u.replace('@', '') for u in username_re.findall(message)
        ]
        return User.objects.filter(username__in = usernames)
    
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
    
    def derive_is_todo(self):
        return todo_re.match(self.message) is not None
    
    def message_without_todo(self):
        return todo_re.sub('', self.message)
    
    def first_on_day(self):
        on_same_day = Blast.objects.filter(
            created__day = self.created.day,
            created__month = self.created.month,
            created__year = self.created.year,
        )
        return on_same_day.filter(created__lt = self.created).count() == 0
    
    def save(self, *args, **kwargs):
        super(Blast, self).save(*args, **kwargs)
        # Update the mentioned users
        self.mentioned_users.clear()
        for user in self.derive_mentioned_users():
            self.mentioned_users.add(user)
        # Is this a todo?
        if self.derive_is_todo() and not self.is_todo:
            self.is_todo = True
            self.save()
    
    class Meta:
        ordering = ('-created',)
    
    def colour(self):
        return md5.new(str(self.user)).hexdigest()[:6]
    
    def __unicode__(self):
        return u'%s at %s' % (self.user, self.created)
    