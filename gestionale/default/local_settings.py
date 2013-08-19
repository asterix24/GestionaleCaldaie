APP_PREFIX_NAME='DEFAULT'

ADMINS = (
    ('Daniele Basile', 'asterix24@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'DB_NAME',           # Or path to database file if using sqlite3.
        'USER': 'DB_USER',                      # Not used with sqlite3.
        'PASSWORD': 'DB_PASS',                  # Not used with sqlite3.
        'HOST': '192.168.10.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'eq2u35)_qf#zrn$n97+o4belkhe9j=xq17yx75f79u*ma*y7wb'
DEBUG = False

LOCAL_ROOT_PATH = 'PWD'
LOCAL_PATH = LOCAL_ROOT_PATH + 'main/templates/' + APP_PREFIX_NAME + '/'
LOCAL_LOG_PATH =  LOCAL_ROOT_PATH + 'log/' + APP_PREFIX_NAME + '/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


# virtual env settings
import os
ENV_PYTHON = "/home/asterix/venv/local/lib/python2.7"
ENV_SITE_PYTHON = os.path.join('/home/asterix/venv/local/lib/python2.7', 'site-packages')

# Email settings
EMAIL_SUBJECT_PREFIX = '[GESTIONEIMPIANTI](DEFAULT) '

DEFAULT_FROM_EMAIL = ''
EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 123

# Define here all specific variable that we want to use
# inside the templates. This dictionary will be merged with
# render context, that is implicit define with render function.
def local_env(request):
    return {"APP_NAME_VERBOSE":"DEFAULT_LONG"}


