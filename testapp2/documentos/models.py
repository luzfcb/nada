from django.db import models
from django.utils.timezone import now

from redactor.fields import RedactorField
import reversion


class TimeStamped(models.Model):
    """
    Provides created and updated timestamps on models.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)


class AbstractDocumento(models.Model):
    conteudo = RedactorField()

    class Meta:
        abstract = True


class Documento(models.Model):
    pass


reversion.register(Documento)
