from bugle.shortcuts import render, redirect, get_object_or_404
from forms import BlastForm
from models import Blast, ImageUpload
from search import query_to_q_object
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.utils import dateformat
from django.template import Template, Context
from django.db.models import Count
from django.utils import simplejson
from django.db.models import Q

import urllib

NUM_ON_HOMEPAGE = 100

class BlastBundle(object):
    is_bundle = True
    
    def __init__(self, blasts):
        self.blasts = blasts
    
    def created(self):
        return self.blasts[0].created
    
    def summary(self):
        return ', '.join([b.short for b in self.blasts])

def prepare_blasts(blasts, user=None, bundle=False):
    blasts = list(blasts.select_related('user'))
    for blast in blasts:
        blast.set_viewing_user(user)
    
    if bundle:
        # Now coagulate chains of blasts with 'short' set in to bundles
        new_blasts = []
        current_bundle = []
        current_bundle_date = None
        for blast in blasts:
            if blast.short and (
                    not current_bundle_date 
                    or blast.created.date() == current_bundle_date
                ):
                current_bundle.append(blast)
                current_bundle_date = blast.created.date()
            else:
                if current_bundle:
                    new_blasts.append(BlastBundle(current_bundle))
                    current_bundle = []
                    current_bundle_date = None
                new_blasts.append(blast)
        
        # Any stragglers?
        if current_bundle:
            new_blasts.append(BlastBundle(current_bundle))
        
        blasts = new_blasts
    
    return blasts

def homepage(request):
    return render(request, 'homepage.html', {
        'blasts': prepare_blasts(
            Blast.objects.all().order_by('-created')[:NUM_ON_HOMEPAGE],
            request.user, bundle=True
        ),
        'more_blasts': Blast.objects.count() > NUM_ON_HOMEPAGE,
        'initial_blast': request.GET.get('blast', ''),
    })

def all(request):
    return render(request, 'homepage.html', {
        'blasts': prepare_blasts(
            Blast.objects.all().order_by('-created'), request.user,
            bundle = True
        ),
        'more_blasts': False,
    })

def blast(request, pk):
    try:
        b = prepare_blasts(
            Blast.objects.filter(pk = pk), request.user
        )[0]
    except IndexError:
        raise Http404
    return render(request, 'blast.html', {
        'blast': b,
        'is_single': True
    })

def post(request):
    if request.user.is_anonymous():
        return redirect('/login/')
    
    form = BlastForm(request.POST, request.FILES)
    if form.is_valid():
        blast = form.save(commit = False)
        if blast.message.startswith('?'):
            return redirect('/search/?' + urllib.urlencode({
                'q': blast.message[1:].strip(),
            }))
        else:
            blast.message = blast.message.strip()
        blast.user = request.user
        blast.save()
    
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
        short = request.POST.get('short', ''),
    )
    return HttpResponse('Message saved')

def post_image(request):
    """Let iPhone Twitter client users attach images"""
    
    image_upload = ImageUpload.objects.create(
        user = request.user,
        attachment = request.FILES['media']
    )
    
    return HttpResponse('<mediaurl>image_upload:%s</mediaurl>' % image_upload.pk)

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
        'blasts': prepare_blasts(
            user.blasts.all(), request.user, bundle=False
        ),
        'show_delete': request.user == user,
    })

def mentions(request, username):
    user = get_object_or_404(User, username = username)
    blasts = Blast.objects.filter(
        Q(mentioned_users = user) | Q(is_broadcast = True)
    ).distinct()
    return render(request, 'mentions.html', {
        'section': 'mentions',
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
        'initial_blast': '@%s ' % username,
    })

def all_mentions(request):
    return render(request, 'all_mentions.html', {
        'section': 'mentions',
        'blasts': prepare_blasts(
            Blast.objects.filter(
                Q(mentioned_users__isnull = False) | Q(is_broadcast = True)
            ).distinct(), request.user
        )
    })

def search(request):
    q = request.GET.get('q', '').strip()
    blasts = []
    if q:
        blasts = prepare_blasts(
            Blast.objects.filter(query_to_q_object(q, 'message')),
            request.user
        )
    return render(request, 'search.html', {
        'q': q,
        'blasts': blasts,
    })

def pastes(request, username):
    user = get_object_or_404(User, username = username)
    blasts = user.blasts.exclude(extended = None).exclude(extended = '')
    return render(request, 'pastes.html', {
        'section': 'pastes',
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
    })

def all_pastes(request):
    return render(request, 'all_pastes.html', {
        'section': 'pastes',
        'blasts': prepare_blasts(
            Blast.objects.exclude(extended=None).exclude(extended=''),
            request.user
        )
    })

def todos(request, username):
    user = get_object_or_404(User, username = username)
    blasts = Blast.objects.filter(is_todo = True).filter(
        Q(user = user) | Q(mentioned_users = user) | Q(is_broadcast = True)
    ).distinct()
    if request.user.username == username:
        initial_blast = 'todo: '
    else:
        initial_blast = 'todo: @%s ' % username
    return render(request, 'todos.html', {
        'section': 'todos',
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
        'initial_blast': initial_blast,
    })

def all_todos(request):
    return render(request, 'all_todos.html', {
        'section': 'todos',
        'blasts': prepare_blasts(
            Blast.objects.filter(is_todo = True), request.user
        ),
        'initial_blast': 'todo: @all ',
    })

def favourites(request, username):
    user = get_object_or_404(User, username = username)
    blasts = Blast.objects.filter(
        favourited_by = user
    )
    return render(request, 'favourites.html', {
        'section': 'favourites',
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
    })

def all_favourites(request):
    return render(request, 'all_favourites.html', {
        'section': 'favourites',
        'blasts': prepare_blasts(
            Blast.objects.filter(
                favourited_by__isnull = False
            ).distinct(), request.user
        )
    })

def files(request, username):
    user = get_object_or_404(User, username = username)
    blasts = user.blasts.exclude(attachment = '')
    return render(request, 'files.html', {
        'section': 'files',
        'profile': user,
        'blasts': prepare_blasts(blasts, request.user),
    })

def all_files(request):
    return render(request, 'all_files.html', {
        'section': 'files',
        'blasts': prepare_blasts(
            Blast.objects.exclude(attachment = ''), request.user
        ),
    })

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


