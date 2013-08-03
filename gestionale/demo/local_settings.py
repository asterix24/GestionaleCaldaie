APP_PREFIX_NAME='demo'

ADMINS = (
    ('Daniele Basile', 'asterix24@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'demo_gestionale',           # Or path to database file if using sqlite3.
        'USER': 'demo',                      # Not used with sqlite3.
        'PASSWORD': 'GJ6aWNp4gTx',                  # Not used with sqlite3.
        'HOST': '192.168.10.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'eq2u35)_qf#zrn$n97+o4belkhe9j=xq17yx75f79u*ma*y7wb'
DEBUG = False

LOCAL_ROOT_PATH = '/home/asterix/gestionale_www/'


LOCAL_PATH = LOCAL_ROOT_PATH + 'main/templates/' + APP_PREFIX_NAME + '/'
LOCAL_LOG_PATH =  LOCAL_ROOT_PATH + 'log/' + APP_PREFIX_NAME + '/'

# virtual env settings
import os
ENV_PYTHON = "/home/asterix/venv/local/lib/python2.7"
ENV_SITE_PYTHON = os.path.join('/home/asterix/venv/local/lib/python2.7', 'site-packages')

# Email settings
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'mail.gandi.net'
#EMAIL_PORT = 465
#EMAIL_HOST_USER = 'error@gestioneimpianti.net'
#EMAIL_HOST_PASSWORD = 'wPqT2zDANS'



