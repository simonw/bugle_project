from django.contrib import admin
from models import Blast

admin.site.register(Blast, search_fields = ('message',))
