# -*- coding: utf8 -*-
from django.apps import AppConfig
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _


def patch_root_urlconf():
    from django.conf.urls import include, url
    from django.core.urlresolvers import clear_url_caches, reverse, NoReverseMatch
    from . import urls
    try:
        reverse('documentos:documento_list')
    except NoReverseMatch:
        urlconf_module = import_module(settings.ROOT_URLCONF)
        urlconf_module.urlpatterns = [
            url(r'^documentos/', include(urls, namespace='documentos')),
        ] + urlconf_module.urlpatterns
        clear_url_caches()


class DocumentosAppConfig(AppConfig):
    name = 'documentos'
    verbose_name = _('Documentos')

    def ready(self):
        patch_root_urlconf()
