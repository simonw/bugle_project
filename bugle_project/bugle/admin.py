from django.contrib import admin
from models import Blast, ImageUpload

admin.site.register(Blast, search_fields = ('message',))
admin.site.register(ImageUpload)
