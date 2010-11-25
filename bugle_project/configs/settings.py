import bugle_project
import os
OUR_ROOT = os.path.realpath(os.path.dirname(bugle_project.__file__))

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'bugle'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(OUR_ROOT, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8-x6*o3&wdi6n!r^td@%nbl*4tt77cc_m)jkb=3enur@c-l+f='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'twitter_api.middleware.ghetto_oauth.GhettoOAuthMiddleware',
#    'debug_middleware.DebugFooter',
)

ROOT_URLCONF = 'bugle_project.urls'

TEMPLATE_DIRS = (
    os.path.join(OUR_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'south',
    'bugle',
    'common',
    'twitter_api',
)

RESERVED_USERNAMES = (
    'admin', 'all', 'toggle', 'favourite', 'favourites', 'stats', 'mentions',
    'pastes', 'paste', 'upload', 'uploads', 'files', 'file', 'images',
    'image', 'photos', 'photo', 'pic', 'todos', 'todo', 'blast', 'blasts',
    'bugle', 'autorefresh', 'ajax', 'polling', 'poll', 'post', 'delete', 
    'account', 'openid', 'logout', 'login', 'static', 'link', 'links',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

SOUTH_TESTS_MIGRATE = True
SKIP_SOUTH_TESTS = True

try:
    from local_settings import *
except ImportError:
    pass

