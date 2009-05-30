from bugle.shortcuts import render, redirect

def homepage(request):
    if request.user.is_anonymous():
        return redirect('/account/register/')
    
    return render(request, 'homepage.html')
