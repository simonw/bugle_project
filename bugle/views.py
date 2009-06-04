from bugle.shortcuts import render, redirect, get_object_or_404
from models import Blast
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import dateformat
from django.template import Template, Context
from django.db.models import Count
import simplejson
from django.db.models import Q

NUM_ON_HOMEPAGE = 50

def prepare_blasts(blasts, user=None):
    blasts = list(blasts)
    for blast in blasts:
        blast.set_viewing_user(user)
    return blasts

def homepage(request, autorefresh=False):
    return render(request, 'homepage.html', {
        'blasts': prepare_blasts(
            Blast.objects.all().order_by('-created')[:NUM_ON_HOMEPAGE],
            request.user
        ),
        'more_blasts': Blast.objects.count() > NUM_ON_HOMEPAGE,
        'autorefresh': autorefresh,
    })

def all(request):
    return render(request, 'homepage.html', {
        'blasts': prepare_blasts(
            Blast.objects.all().order_by('-created'), request.user
        ),
        'more_blasts': False,
        'autorefresh': False,
    })

def blast(request, pk):
    return render(request, 'blast.html', {
        'blast': prepare_blasts(
            [get_object_or_404(Blast, pk = pk)], request.user
        )[0],
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
        'blasts': prepare_blasts(user.blasts.all(), request.user),
        'show_delete': request.user == user,
    })

def mentions(request, username):
    user = get_object_or_404(User, username = username)
    blasts = user.mentions.all()
    return render(request, 'mentions.html', {
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
    })

def all_mentions(request):
    return render(request, 'all_mentions.html', {
        'blasts': prepare_blasts(
            Blast.objects.filter(mentioned_users__isnull = False),
            request.user
        )
    })

def pastes(request, username):
    user = get_object_or_404(User, username = username)
    blasts = user.blasts.exclude(extended = None).exclude(extended = '')
    return render(request, 'pastes.html', {
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
    })

def all_pastes(request):
    return render(request, 'all_pastes.html', {
        'blasts': prepare_blasts(
            Blast.objects.exclude(extended=None).exclude(extended=''),
            request.user
        )
    })

def todos(request, username):
    user = get_object_or_404(User, username = username)
    blasts = Blast.objects.filter(is_todo = True).filter(
        Q(user = user) | Q(mentioned_users = user)
    ).distinct()
    return render(request, 'todos.html', {
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
    })

def all_todos(request):
    return render(request, 'all_todos.html', {
        'blasts': prepare_blasts(
            Blast.objects.filter(is_todo = True), request.user
        )
    })

def favourites(request, username):
    user = get_object_or_404(User, username = username)
    blasts = Blast.objects.filter(
        user = user,
        favourited_by__isnull = False
    )
    return render(request, 'favourites.html', {
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
    })

def all_favourites(request):
    return render(request, 'all_favourites.html', {
        'blasts': prepare_blasts(
            Blast.objects.filter(favourited_by__isnull = False), request.user
        )
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
    key = [k for k in request.POST.keys() if 'check' in k][0].split('.')[0]
    # key will now be uncheck-45 or check-23
    verb, pk = key.split('-')
    blast = get_object_or_404(Blast, pk = pk)
    # Check the user is allowed to modify this blast
    blast.set_viewing_user(request.user)
    if not blast.viewing_user_can_mark_done():
        return HttpResponse('You are not allowed to check off that task')
    if verb == 'check':
        blast.done = True
    if verb == 'uncheck':
        blast.done = False
    blast.save()
    return redirect(request.POST.get('back_to', '') or '/')

def favourite(request):
    if request.user.is_anonymous():
        return redirect('/login/')
    key = [k for k in request.POST.keys() if 'fave' in k][0].split('.')[0]
    # key will now be uncheck-45 or check-23
    verb, pk = key.split('-')
    blast = get_object_or_404(Blast, pk = pk)
    # Check the user is allowed to modify this blast
    blast.set_viewing_user(request.user)
    if not blast.user_can_favourite():
        return HttpResponse('You are not allowed to favourite that')
    if verb == 'fave':
        blast.favourited_by.add(request.user)
    if verb == 'notfave':
        blast.favourited_by.remove(request.user)
    return redirect(request.POST.get('back_to', '') or '/')
