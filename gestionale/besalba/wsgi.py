"""
WSGI config for gestionale project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import sys
import site
import os
import local_settings

site.addsitedir(local_settings.ENV_PYTHON)
site.addsitedir(local_settings.ENV_SITE_PYTHON)
sys.path.append(local_settings.LOCAL_ROOT_PATH)

os.environ["DJANGO_SETTINGS_MODULE"] = "gestionale.besalba.settings"

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
