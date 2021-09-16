from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('taskName', css_class='form-control'),
            Field('fleetNumber', css_class='form-control'),
            Field('group', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = TaskModel
        fields = ['taskName', 'fleetNumber', 'group']

class TaskUserForm(TaskForm):



    class Meta:
        model = TaskPartsModel
        fields = ['user']


class TaskActivityPartsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskActivityPartsForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.fields['serial'].required = False
        self.fields['extra'].required = False
        self.helper.layout = Layout(
            Field('activity', type='hidden'),
            Field('part', css_class='form-control'),
            Field('task', type='hidden'),
            Field('increment', type='hidden'),
            Field('quantityRequired', css_class='form-control'),
            Field('quantityCompleted', type='hidden'),
            Field('user', type='hidden'),
            Field('serial', type='form-control'),
            Field('extra', type='form-control'),
            Field('order', type='hidden'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = TaskPartsModel
        fields = '__all__'

class TaskActivitiesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskActivitiesForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.fields['finishTime'].required = False
        self.helper.layout = Layout(
            Field('task', type='hidden'),
            Field('activity', css_class='form-control'),
            Field('startTime', type='hidden'),
            Field('finishTime', type='hidden'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = TaskActivityModel
        fields = '__all__'