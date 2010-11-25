#!/usr/bin/env python
import os
import site
import sys

prev_sys_path = list(sys.path) 

site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), '../bugle_project_ve/lib/python%s/site-packages' % '.'.join((unicode(x) for x in sys.version_info[0:2])))))

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item) 
        sys.path.remove(item) 
sys.path[:0] = new_sys_path

from django.core.management import execute_manager
try:
    from bugle_project.configs import settings
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)

