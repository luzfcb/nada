from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views import generic
from reversion.models import Version

from .models import Artigo
from .forms import ArtigoForm

import reversion





class VersionListMixin(generic.UpdateView):
    def get_context_data(self, **kwargs):
        context = super(VersionListMixin, self).get_context_data(**kwargs)
        version_list = reversion.get_unique_for_object(self.get_object())
        context.update(
            {
                'version_list': version_list
            }
        )
        print(type(version_list))
        print(version_list)
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

# class ArtigoVersionsList(generic.ListView):



class RevisionView(generic.DetailView):
    model = Version



    # def get_object(self, queryset=None):
    #     return super(RevisionView, self).get_object(queryset)


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


