from django.contrib import admin

from .models import Artigo

from reversion import VersionAdmin


@admin.register(Artigo)
class ArtigoAdmin(VersionAdmin):
    list_display = ['conteudo', ]

