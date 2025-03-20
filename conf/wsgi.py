"""
    WSGI config for Django-Bom
    --------------------------
    This file is used to start the Django application using WSGI servers
    like Gunicorn under YunoHost.
"""

import os
from django.core.wsgi import get_wsgi_application

# Définir les paramètres Django si non définis
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_bom.settings')

# Création de l'application WSGI
application = get_wsgi_application()
