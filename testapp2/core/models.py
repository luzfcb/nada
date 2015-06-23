# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
import reversion


class TimeStamped(models.Model):
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('criado em')
    )

    modificado_em = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modificado em'),
        help_text=_('Data e horario da ultima modificação')
    )

    class Meta:
        abstract = True

class ConteudoMixin(models.Model):

    conteudo = models.TextField(
        verbose_name=_('Conteúdo')
    )

    class Meta:
        abstract = True


@reversion.register
class Artigo(ConteudoMixin, TimeStamped):
    pass

