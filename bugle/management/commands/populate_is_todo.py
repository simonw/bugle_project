from django.core.management.base import BaseCommand, CommandError
from bugle.models import Blast
from django.contrib.auth.models import User
import re, sys

class Command(BaseCommand):
    help = """
    Ensures that all @username mentions are added to the mentions DB table
    """.strip()
    
    requires_model_validation = True
    can_import_settings = True
    
    def handle(self, *args, **options):
        if len(args) != 0:
            raise CommandError("Command doesn't accept any arguments")
        
        for blast in Blast.objects.all():
            blast.is_todo = blast.derive_is_todo()
            blast.save()
            sys.stdout.write('.')
        sys.stdout.write(' done\n')
