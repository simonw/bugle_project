from bugle.shortcuts import render, redirect, get_object_or_404
from models import Blast
from django.contrib.auth.models import User

def homepage(request):
    if request.user.is_anonymous():
        return redirect('/login/')
    
    return render(request, 'homepage.html', {
        'blasts': Blast.objects.all().order_by('-created')[:30],
    })

def post(request):
    if request.user.is_anonymous():
        return redirect('/login/')
    message = request.POST.get('blast', '').strip()
    if message:
        Blast.objects.create(
            user = request.user,
            message = message
        )
    return redirect('/')

def profile(request, username):
    user = get_object_or_404(User, username = username)
    return render(request, 'profile.html', {
        'profile': user,
    })
