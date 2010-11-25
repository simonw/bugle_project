from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from registration.forms import RegistrationForm

def register(request, next=settings.LOGIN_REDIRECT_URL, form_cls=RegistrationForm,
             profile_cb=None, login_cb=None, template='registration/register.html',
             extra_context=None, initial=None):
    """
    Register user by e-mail address and log them in.
    
    """
    if request.method == "POST":
        form = form_cls(request.POST)
        if form.is_valid():
            user, pw = form.save(request, profile_cb)
            user = auth.authenticate(username=user.username, password=pw)
            auth.login(request, user)
            response = HttpResponseRedirect(next)
            if login_cb is not None:
                response = login_cb(response, user)
            return response

    else:
        form = form_cls(initial=initial)

    context = {'form': form}    
    if extra_context is not None:
        context.update(extra_context)        

    return render_to_response(template, context, RequestContext(request))
