import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../bugle_project/")))

os.environ["DJANGO_SETTINGS_MODULE"] = "bugle_project.settings"
 
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()


