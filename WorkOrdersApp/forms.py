from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field,Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class WorkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('vehicle', css_class='form-control'),
            Field('task', css_class='form-control'),
            Field('activity', css_class='form-control'),
            Field('part', css_class='form-control'),
            Field('increment', css_class='form-control'),
            Field('quantityRequired', css_class='form-control'),
            Field('quantityCompleted', css_class='form-control'),
            Field('user', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = WorkCentreModel
        fields = ['vehicle', 'task']
