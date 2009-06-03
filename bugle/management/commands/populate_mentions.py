from django.core.management.base import BaseCommand, CommandError
from bugle.models import Blast
from django.contrib.auth.models import User
import re, sys

username_re = re.compile('@[0-9a-zA-Z]+')

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
            usernames = [
                u.replace('@', '') for u in username_re.findall(blast.message)
            ]
            users = User.objects.filter(username__in = usernames)
            blast.mentioned_users.clear()
            for u in users:
                blast.mentioned_users.add(u)
            sys.stdout.write('.')
        sys.stdout.write(' done\n')
