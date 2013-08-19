import os
if os.environ["DJANGO_SETTINGS_MODULE"] == "gestionale.besalba.settings":
    from besalba import local_settings
    from besalba import settings
    from besalba.local_settings import local_env
if os.environ["DJANGO_SETTINGS_MODULE"] == "gestionale.demo.settings":
    from demo import local_settings
    from demo import settings
    from demo.local_settings import local_env
