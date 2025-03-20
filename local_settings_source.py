# This file will be copied to the "local test" files, to overwrite Django settings for Django-Bom

import os

print('Loading local settings file:', __file__)

ENV_TYPE = os.environ.get('ENV_TYPE', 'production')  # Default to production
print(f'ENV_TYPE: {ENV_TYPE!r}')

# General settings
DEBUG = ENV_TYPE in ['local', 'test']

if ENV_TYPE == 'local':
    print('Running in local development mode')
    
    # Allow connections from localhost
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    
    # Disable SSL redirect for local dev
    SECURE_SSL_REDIRECT = False  
    
    # Serve static/media files directly (useful for dev)
    SERVE_FILES = True  

    # Disable password validation for dev
    AUTH_PASSWORD_VALIDATORS = []

elif ENV_TYPE == 'test':
    print('Running in test mode')
    
    # Silence security warnings for tests
    SILENCED_SYSTEM_CHECKS = ['security.W018']

    # Allow test framework to set hosts
    ALLOWED_HOSTS = []

elif ENV_TYPE == 'production':
    print('Running in production mode')
    
    # YunoHost domain settings
    YNH_DOMAIN = os.environ.get('YNH_APP_ARG_DOMAIN', 'your-domain.tld')
    ALLOWED_HOSTS = [YNH_DOMAIN]

    # Enforce SSL redirect
    SECURE_SSL_REDIRECT = True

# Database settings for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'django_bom_db'),
        'USER': os.environ.get('POSTGRES_USER', 'django_bom_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Caching (Using local memory cache for local/testing environments)
if ENV_TYPE in ['local', 'test']:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        },
    }
