import os
if os.environ["DJANGO_SETTINGS_MODULE"] == "gestionale.besalba.settings":
    from besalba import local_settings
if os.environ["DJANGO_SETTINGS_MODULE"] == "gestionale.demo.settings":
    from demo import local_settings
