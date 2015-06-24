# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip
from django.contrib.contenttypes.fields import GenericRelation

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
import reversion
from django.db import transaction
from reversion.models import Version


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

    versions = GenericRelation(Version)

    class Meta:
        abstract = True


@reversion.register
class Artigo(ConteudoMixin, TimeStamped):
    pass




class VersionMixin(object):
    def creator(self):
        version_list = reversion.get_for_object(self)
        return version_list.earliest('revision__date_created').revision.user

    def modifier(self):
        version_list = reversion.get_for_object(self)
        return version_list.latest('revision__date_created').revision.user

    def date_created(self):
        version_list = reversion.get_for_object(self)
        return version_list.earliest('revision__date_created').revision.date_created

    def date_modified(self):
        version_list = reversion.get_for_object(self)
        return version_list.latest('revision__date_created').revision.date_created

    def latest_version(self):
        version_list = reversion.get_for_object(self)
        return version_list.latest('revision__date_created').pk

    def versions(self):
        version_list = reversion.get_for_object(self)
        return version_list

    def nr_of_versions(self):
        version_list = reversion.get_for_object(self)
        return len(version_list)

    def save_revision(self, user, comment, *args, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            self.save()
            if user.is_authenticated():
                reversion.set_user(user)
            reversion.set_comment(comment)
