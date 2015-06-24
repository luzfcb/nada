from django import forms
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views import generic
from reversion.models import Version

from .models import Artigo
from .forms import ArtigoForm, ReverterHelper

import reversion


class VersionListMixin(object):
    def get_context_data(self, **kwargs):
        context = super(VersionListMixin, self).get_context_data(**kwargs)
        version_list = reversion.get_unique_for_object(self.get_object())
        context.update(
            {
                'version_list': version_list
            }
        )

        return context


class ArtigoListView(generic.ListView):
    model = Artigo


class ArtigoCreateView(generic.CreateView):
    model = Artigo
    success_url = reverse_lazy('artigo_list')
    form_class = ArtigoForm


class ArtigoUpdateView(VersionListMixin, generic.UpdateView):
    model = Artigo
    success_url = reverse_lazy('artigo_list')
    form_class = ArtigoForm

    def get_context_data(self, **kwargs):
        contexto = super(ArtigoUpdateView, self).get_context_data(**kwargs)
        versoes = self.get_object().versions.all()
        versoes_unicas = reversion.get_unique_for_object(self.get_object())
        total_versoes = versoes.count()

        z = versoes_unicas[0]
        contexto.update(
            {
                'versoes': versoes,
                'versoes_unicas': versoes_unicas,
                'total_versoes': total_versoes,
                'z': z.field_dict,
                'zz': ArtigoForm(initial=z.field_dict)
            }
        )
        return contexto


# class ArtigoVersionsList(generic.ListView):



class ReverterForm(forms.Form):
    comentario = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.original = forms.ModelChoiceField(queryset=None, initial=kwargs.get('modelo', None))
        super(ReverterForm, self).__init__(*args, **kwargs)
        self.helper = ReverterHelper(self)



class RevisionView(generic.FormView, generic.DetailView):
    model = Version
    form_class = ReverterForm

    def get(self, request, *args, **kwargs):
        return super(RevisionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexto = super(RevisionView, self).get_context_data(**kwargs)
        contexto.update(
            {'form': self.form_class
             }
        )
        return contexto

    def get_form_class(self):
        class A(ReverterForm, ArtigoForm):
            pass
        return A

    def get_initial(self):
        initial = super(RevisionView, self).get_initial()
        initial.update(
            self.get_object().field_dict
        )
        return initial

    def form_valid(self, form):
        value = super(RevisionView, self).form_valid(form)
        z = self.get_object().revert()
        print(z)
        reversion.set_user(self.request.user)
        reversion.set_comment(form.cleaned_data.get('comentario', 'NADA'))
        return value

    def get_success_url(self):
        return reverse_lazy('artigo_update',
                            kwargs={
                                'pk': self.get_object().object_id
                            }
                            )


import reversion
from django.db import transaction


class ReversionViewMixin(object):
    def dispatch(self, *args, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            return super(ReversionViewMixin, self).dispatch(*args, **kwargs)


class ReversionSerializerMixin(object):
    def create(self, *args, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            return super(ReversionSerializerMixin, self).create(*args, **kwargs)

    def update(self, *args, **kwargs):
        with transaction.atomic(), reversion.create_revision():
            return super(ReversionSerializerMixin, self).update(*args, **kwargs)
