from django.conf import settings

def faye_url(request):
    return {'FAYE_URL': settings.FAYE_URL}

