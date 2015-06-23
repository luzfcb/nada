from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


# place form definition here
from django import forms
from .models import Artigo


class SaveHelper(FormHelper):
    def __init__(self, form=None):
        super(SaveHelper, self).__init__(form)
        self.layout.append(Submit(name='save', value='Salvar'))
        self.form_show_errors = True
        self.render_required_fields = True



class ArtigoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArtigoForm, self).__init__(*args, **kwargs)
        self.helper = SaveHelper(self)

    class Meta:
        model = Artigo
        fields = '__all__'
