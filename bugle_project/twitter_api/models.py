from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
import md5
from PIL import Image
import StringIO

class TwitterProfile(models.Model):
    user = models.OneToOneField(User, related_name='twitter_profile')
    profile_image = models.ImageField(upload_to='profile-images/')

    def save(self, *args, **kwargs):
        if not self.profile_image:
            im = Image.new('RGB', (48, 48), '#%s' % md5.new(str(self.user)).hexdigest()[:6])
            output = StringIO.StringIO()
            im.save(output, format='PNG')
            self.profile_image.save(
                '%s.png' % self.user.id,
                ContentFile(output.getvalue()),
                save=False,
            )
        super(TwitterProfile, self).save(*args, **kwargs)

