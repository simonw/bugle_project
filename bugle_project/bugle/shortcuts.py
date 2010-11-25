from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

def render(request, template_name, context=None, base=None):
    context = context or {}
    context['base'] = base or 'base.html'
    context['path'] = request.path
    return render_to_response(
        template_name, context, context_instance = RequestContext(request)
    )

redirect = HttpResponseRedirect