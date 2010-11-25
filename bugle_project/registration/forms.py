from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

import re
username_re = re.compile('^[a-zA-Z0-9]+$')

class RegistrationForm(forms.Form):
    """
    Registration form for new users.
    
    """
    username     = forms.CharField(label=_("Username"), max_length=30)
    password1 = forms.CharField(label=_("Password"), max_length=16, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password Confirmation"), max_length=16, widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data.get("username").lower()
        if username in getattr(settings, 'RESERVED_USERNAMES', []):
            raise forms.ValidationError(_(
                'That username cannot be registered'
            ))
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            if not username_re.match(username):
                raise forms.ValidationError(_(
                    "Invalid username - try something that would work in a URL"
                ))

            return username
        raise forms.ValidationError(_("There is already a user with this username."))
    
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data

    def save(self, request, profile_cb=None):
        
        args = [
            self.cleaned_data["username"],
            self.cleaned_data["username"] + '@example.com',
            self.cleaned_data["password1"]
        ]
        user = User.objects.create_user(*args)
        
        if profile_cb is not None:
            profile_cb(user)
        
        # Return p/w so we can log the dude in.
        return user, self.cleaned_data["password1"]
