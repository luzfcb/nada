from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Documento

from reversion_extras.views import DetailVersionListView
from core.forms import Submit

class DocumentoListView(generic.ListView):
    model = Documento


class DocumentoCreateView(generic.CreateView):
    model = Documento
    fields = '__all__'
    success_url = reverse_lazy('documento_list')


class DocumentoUpdateView(generic.UpdateView):
    model = Documento
    fields = '__all__'
    success_url = reverse_lazy('documento_list')


class DocumentoVersionsView(DetailVersionListView):
    model = Documento
    fields = '__all__'
    success_url = reverse_lazy('documento_list')
