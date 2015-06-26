from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.views.generic.detail import SingleObjectMixin, BaseDetailView
import pycallgraph
from pycallgraph.output import GraphvizOutput
from reversion.models import Version
from .list import DetailVersionListViewMixin

from .models import Artigo
from .forms import ArtigoForm, ReverterHelper, ReadOnlyAllFieldsMixin

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
    template_name = 'core/artigo_form2.html'
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
        super(ReverterForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'helper'):
            self.helper.layout.append(Submit(name='reverter', value='Reverter'))
        else:
            self.helper = ReverterHelper(self)


class RevisionView(generic.DetailView, SingleObjectMixin):
    model = Version
    # form_class = ReverterForm

    # def get(self, request, *args, **kwargs):
    #     return super(RevisionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contexto = super(RevisionView, self).get_context_data(**kwargs)
        contexto.update(
            {'form': self.form_class
             }
        )

        return contexto

    def get_form_class(self):
        class A(ReadOnlyAllFieldsMixin, ReverterForm, ArtigoForm):
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
        self.get_object().revert()
        reversion.set_user(self.request.user)
        reversion.set_comment(form.cleaned_data.get('comentario', 'NADA'))
        return value

    def get_success_url(self):
        return reverse_lazy('artigo_update',
                            kwargs={
                                'pk': self.get_object().object_id
                            }
                            )


class GenericRevisionView(generic.FormView, BaseDetailView):

    version_list = None
    model = Version
    model_to_revision = None
    template_name = 'core/artigo_form.html'

    def get_model_to_revision(self):
        if self.model_to_revision is None:
            raise ImproperlyConfigured(
                '{0} is missing a model_to_revision '
                'name to reverse and redirect to. Define '
                '{0}.model_to_revision or override '
                '{0}.get_model_to_revision().'.format(self.__class__.__name__))
        return self.model_to_revision

    def __init__(self, **kwargs):
        super(GenericRevisionView, self).__init__(**kwargs)
        if self.form_class:
            class GenericRevisionForm(ReadOnlyAllFieldsMixin, self.form_class):
                class Meta:
                    model = self.get_model_to_revision()
                    fields = '__all__'

            self.form_class = GenericRevisionForm

    def get(self, request, *args, **kwargs):
        a = super(GenericRevisionView, self).get(request, *args, **kwargs)
        self.version_list = reversion.get_unique_for_object(self.get_object())
        context = self.get_context_data(version_list=self.version_list)
        return self.render_to_response(context)
        # return



class RevisionView2(GenericRevisionView):
    pass




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





class ArtigoVersionListView(DetailVersionListViewMixin):
    model = Artigo
    version_paginate_by = 2
    def __init__(self, **kwargs):
        super(ArtigoVersionListView, self).__init__(**kwargs)
