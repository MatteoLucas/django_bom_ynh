"""
    Gunicorn Configuration for Django-Bom
    -------------------------------------
    Optimized for use with YunoHost and Nginx.
"""

import multiprocessing
import os

# Utiliser un socket Unix pour de meilleures performances avec Nginx
bind = 'unix:/run/django-bom.sock'

# Nombre optimal de workers basé sur le CPU
workers = multiprocessing.cpu_count() * 2 + 1

# Niveau de log
loglevel = 'info'

# Fichiers de logs
LOG_FILE = os.getenv('LOG_FILE', '/var/log/django-bom/gunicorn.log')
accesslog = LOG_FILE
errorlog = LOG_FILE

# Fichier PID
DATA_DIR = os.getenv('DATA_DIR', '/home/yunohost.app/django-bom')
pidfile = f"{DATA_DIR}/gunicorn.pid"
