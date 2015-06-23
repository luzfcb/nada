# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artigo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('modificado_em', models.DateTimeField(help_text='Data e horario da ultima modifica\xe7\xe3o', verbose_name='modificado em', auto_now=True)),
                ('conteudo', models.TextField(verbose_name='Conte\xfado')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
