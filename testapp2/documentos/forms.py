from django import forms
from core.forms import SalvarFormMixin
from .models import Documento


class DocumentoForm(SalvarFormMixin, forms.ModelForm):

    class Meta:
        model = Documento
        fields = '__all__'
