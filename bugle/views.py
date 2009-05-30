from bugle.shortcuts import render, redirect
from models import Blast

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

