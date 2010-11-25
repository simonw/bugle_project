import os
import site
import sys

project_name = 'bugle_project'

prev_sys_path = list(sys.path) 

site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../%s_ve/lib/python2.5/site-packages' % project_name)))

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path

os.environ["DJANGO_SETTINGS_MODULE"] = "%s.configs.live.settings" % project_name
 
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

