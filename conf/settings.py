################################################################################
# Django-Bom YunoHost Settings
################################################################################

import os
from pathlib import Path

# Directories
DATA_DIR_PATH = Path(os.getenv('DATA_DIR', '/home/yunohost.app/django-bom'))
INSTALL_DIR_PATH = Path(os.getenv('INSTALL_DIR', '/var/www/django-bom'))

LOG_FILE_PATH = Path(os.getenv('LOG_FILE', f'/var/log/django-bom/django-bom.log'))

# YunoHost Domain and Path
YNH_CURRENT_HOST = os.getenv('YNH_CURRENT_HOST', 'localhost')
PATH_URL = os.getenv('PATH', '').strip('/')

# -------------------------------------------------------------------
# DEBUG & LOGGING SETTINGS (From YunoHost Panel)
# -------------------------------------------------------------------
DEBUG = os.getenv('DEBUG_ENABLED', '0') == '1'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')

# -------------------------------------------------------------------
# DATABASE CONFIGURATION (POSTGRESQL)
# -------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django_bom_db'),
        'USER': os.getenv('POSTGRES_USER', 'django_bom_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

# -------------------------------------------------------------------
# EMAIL CONFIGURATION
# -------------------------------------------------------------------
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', f'admin@{YNH_CURRENT_HOST}')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', f'django-bom@{YNH_CURRENT_HOST}')
SERVER_EMAIL = ADMIN_EMAIL

ADMINS = (('Admin', ADMIN_EMAIL),)
MANAGERS = ADMINS

# -------------------------------------------------------------------
# DOMAIN & SECURITY SETTINGS
# -------------------------------------------------------------------
SITE_DOMAIN = os.getenv('DOMAIN', YNH_CURRENT_HOST)

ALLOWED_HOSTS = [SITE_DOMAIN]
if PATH_URL:
    ALLOWED_HOSTS.append(f"{SITE_DOMAIN}/{PATH_URL}")

# -------------------------------------------------------------------
# AUTHENTICATION & LOGIN (SSO)
# -------------------------------------------------------------------
LOGIN_URL = '/yunohost/sso/'
LOGOUT_REDIRECT_URL = '/yunohost/sso/'
LOGIN_REDIRECT_URL = None

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# -------------------------------------------------------------------
# STATIC & MEDIA FILES CONFIGURATION
# -------------------------------------------------------------------
STATIC_URL = f'/{PATH_URL}/static/' if PATH_URL else '/static/'
MEDIA_URL = f'/{PATH_URL}/media/' if PATH_URL else '/media/'

STATIC_ROOT = str(INSTALL_DIR_PATH / 'static')
MEDIA_ROOT = str(INSTALL_DIR_PATH / 'media')

# -------------------------------------------------------------------
# LOGGING CONFIGURATION
# -------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': str(LOG_FILE_PATH),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': LOG_LEVEL,
    },
}

# -------------------------------------------------------------------
# LOAD LOCAL SETTINGS IF AVAILABLE
# -------------------------------------------------------------------
try:
    from local_settings import *  # noqa:F401,F403
except ImportError:
    pass
