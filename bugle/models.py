from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import md5, re

todo_re = re.compile(r'\btodo:', re.I)
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
    
    def viewing_user(self):
        """We often need to make template decisions based on the user VIEWING
        the blast"""
        return getattr(self, '_viewing_user', None)
    
    def set_viewing_user(self, user):
        self._viewing_user = user
        # Cache user favourites
        user.cached_fave_ids = user.favourites.values_list('pk', flat = True)
    
    def viewing_user_is_owner(self):
        return self.viewing_user() == self.user
    
    def viewing_user_can_mark_done(self):
        allowed = [self.user] + list(self.mentioned_users.all())
        return self.viewing_user() in allowed
    
    def derive_mentioned_users(self, message=None):
        "Figure out mentioned users just from the message text"
        if message is None:
            message = self.message
        usernames = [
            u.replace('@', '') for u in username_re.findall(message)
        ]
        return User.objects.filter(username__in = usernames)
    
    def checkbox_img_name(self):
        return self.done and 'checked' or 'unchecked'
    
    def checkbox_verb(self):
        return self.done and 'uncheck' or 'check'
    
    def checkbox_img(self):
        return mark_safe(
        '<img src="/static/img/%(img)s.png" alt="%(img)s" class="donebox">'%{
            'img': self.done and 'checked' or 'unchecked',
        })
    
    def user_can_favourite(self):
        return self.viewing_user() is not None and \
            not self.viewing_user().is_anonymous()
    
    def is_favourited(self):
        if not self.user_can_favourite():
            return False
        return self.pk in self.viewing_user().cached_fave_ids
    
    def favourite_verb(self):
        return self.is_favourited() and 'notfave' or 'fave'
    
    def favourite_img_name(self):
        return self.is_favourited() and 'fave' or 'notfave'
    
    def derive_is_todo(self):
        return todo_re.search(self.message) is not None
    
    def message_without_todo(self):
        remove = 'todo:'
        if self.message.startswith(remove):
            return self.message[len(remove):]
        return self.message
    
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
    