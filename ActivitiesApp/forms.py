from django import forms
from .models import ActivityModel, ActivityPartModel, TaskModel, TaskActivityModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field,Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class activity_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(activity_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('activityName', css_class='form-control'),
            Field('description', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = ActivityModel
        fields = '__all__'


class required_part_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(required_part_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('activity', type='hidden'),
            Field('part', css_class='form-control'),
            Field('quantity', css_class='form-control'),
            Field('increment', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = ActivityPartModel
        fields = '__all__'


class task_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(task_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('taskName', css_class='form-control'),
            Submit('save', 'Save')
        )

    class Meta:
        model = TaskModel
        fields = ['taskName']


class required_activity_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(required_activity_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('task', type="hidden"),
            Field('activity', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = TaskActivityModel
        fields = '__all__'
