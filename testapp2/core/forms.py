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


class ReverterHelper(FormHelper):
    def __init__(self, form=None):
        super(ReverterHelper, self).__init__(form)
        self.layout.append(Submit(name='reverter', value='Reverter'))
        self.form_show_errors = True
        self.render_required_fields = True


class SalvarFormMixin(object):
    def __init__(self, *args, **kwargs):
        super(SalvarFormMixin, self).__init__(*args, **kwargs)
        self.helper = SaveHelper(self)


class ArtigoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArtigoForm, self).__init__(*args, **kwargs)
        self.helper = SaveHelper(self)

    class Meta:
        model = Artigo
        fields = '__all__'


class ReadOnlyFieldsMixin(object):
    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        for field in (field for name, field in self.fields.iteritems() if
                      name in self.readonly_fields):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        cleaned_data = super(ReadOnlyFieldsMixin, self).clean()
        for field in self.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data


class ReadOnlyAllFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super(ReadOnlyAllFieldsMixin, self).__init__(*args, **kwargs)
        for field in (field for name, field in self.fields.iteritems()):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        cleaned_data = super(ReadOnlyAllFieldsMixin, self).clean()
        for field in self.fields:
            cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data
