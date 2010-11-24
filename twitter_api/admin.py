from bugle_project.twitter_api.models import TwitterProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class TwitterProfileInline(admin.StackedInline):
    model = TwitterProfile
    extra = 1
    max_num = 1

class TwitterProfileUserAdmin(UserAdmin):
    inlines = [TwitterProfileInline]

admin.site.unregister(User)
admin.site.register(User, TwitterProfileUserAdmin)

