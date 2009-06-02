from bugle.shortcuts import render, redirect, get_object_or_404
from models import Blast
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import dateformat
from django.template import Template, Context
from django.db.models import Count
import simplejson

NUM_ON_HOMEPAGE = 50

def homepage(request, autorefresh=False):
    return render(request, 'homepage.html', {
        'blasts': Blast.objects.all().order_by('-created')[:NUM_ON_HOMEPAGE],
        'more_blasts': Blast.objects.count() > NUM_ON_HOMEPAGE,
        'autorefresh': autorefresh,
    })

def all(request):
    return render(request, 'homepage.html', {
        'blasts': Blast.objects.all().order_by('-created'),
        'more_blasts': False,
        'autorefresh': False,
    })

def blast(request, pk):
    return render(request, 'blast.html', {
        'blast': get_object_or_404(Blast, pk = pk),
    })

def post(request):
    if request.user.is_anonymous():
        return redirect('/login/')
    message = request.POST.get('blast', '').strip()
    if message:
        Blast.objects.create(
            user = request.user,
            message = message,
            extended = request.POST.get('extended', ''),
        )
    return redirect('/')

def post_api(request):
    username = request.POST.get('username', '')
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        return HttpResponse('Invalid username')
    
    if not user.check_password(request.POST.get('password', '')):
        return HttpResponse('Invalid password')
    
    message = request.POST.get('message', '').strip()
    if not message:
        return HttpResponse('Invalid message')
    
    Blast.objects.create(
        user = user,
        message = message,
        extended = request.POST.get('extended', ''),
    )
    return HttpResponse('Message saved')

def delete(request):
    if request.user.is_anonymous():
        return redirect('/login/')
    
    blast = get_object_or_404(Blast, pk = request.POST.get('id', ''))
    if blast.user == request.user:
        blast.delete()
    
    return redirect('/%s/' % request.user)

def profile(request, username):
    user = get_object_or_404(User, username = username)
    return render(request, 'profile.html', {
        'profile': user,
        'is_own_profile': user == request.user
    })

def mentions(request, username):
    user = get_object_or_404(User, username = username)
    blasts = Blast.objects.filter(message__contains = '@' + username)
    return render(request, 'mentions.html', {
        'profile': user,
        'blasts': blasts,
    })

message_template = Template("{% load bugle %}{{ msg|urlize|buglise }}")

def since(request):
    id = request.GET.get('id', 0)
    blasts = Blast.objects.filter(id__gt = id).order_by('-created')
    return HttpResponse(simplejson.dumps([{
        'user': str(b.user),
        'message': message_template.render(Context({
            'msg': b.message,
        })),
        'created': str(b.created),
        'date': dateformat.format(b.created, 'jS F'),
        'time': dateformat.format(b.created, 'H:i'),
        'colour': '#' + b.colour(),
        'id': b.id,
        'first_on_day': b.first_on_day(),
    } for b in blasts]), content_type = 'text/plain')

def stats(request):
    blast_dates = list(Blast.objects.values_list('created', flat=True))
    date_counts = {}
    for date in blast_dates:
        d = date.date()
        date_counts[d] = date_counts.get(d, 0) + 1
    top_dates = date_counts.items()
    top_dates.sort(key = lambda x: x[0])
    return render(request, 'stats.html', {
        'top_users': User.objects.annotate(
            num_blasts = Count('blasts')
        ).order_by('-num_blasts'),
        'top_dates': top_dates,
    })

def toggle(request):
    if request.user.is_anonymous():
        return redirect('/login/')
    key = request.POST.keys()[0].split('.')[0]
    # key will now be uncheck-45 or check-23
    verb, pk = key.split('-')
    blast = get_object_or_404(Blast, pk = pk, user = request.user)
    if verb == 'check':
        blast.done = True
    if verb == 'uncheck':
        blast.done = False
    blast.save()
    return redirect('/')
