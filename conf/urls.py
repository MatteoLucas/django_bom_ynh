"""
    urls.py - Django-Bom YunoHost URL configuration
"""

from django.conf import settings
from django.urls import include, path
from django.views.generic import RedirectView

if settings.PATH_URL:
    # Si Django-Bom est installé dans un sous-dossier (ex: /django-bom)
    urlpatterns = [
        path('', RedirectView.as_view(url=f'/{settings.PATH_URL}/', permanent=True)),
        path(f'{settings.PATH_URL}/', include('django_bom.urls')),
    ]
else:
    # Si Django-Bom est installé à la racine du domaine
    from django_bom.urls import urlpatterns  # noqa
