from django import forms
from django.forms import HiddenInput

from .models import ActivityModel, ActivityPartModel, GroupModel, GroupActivityModel, instruction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Hidden, Column
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class activity_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(activity_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(
            Field('activityName', css_class='form-control'), css_class='col-md-6'
                ),
                Column('workCenter'),
                Column(Submit('save', 'Save'), css_class="btn col-md-2")
            ),
            Field('description', css_class='form-control'),
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
            Field('increment', type='hidden'),
            HTML('<br>'),
            Submit('save', 'Add to Activity')
        )

    class Meta:
        model = ActivityPartModel
        fields = ['activity', 'part', 'quantity', 'increment']


class group_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(group_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('groupName', css_class='form-control'),
            Submit('save', 'Save')
        )

    class Meta:
        model = GroupModel
        fields = ['groupName']


class required_activity_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(required_activity_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('group', type="hidden"),
            Field('order', type="hidden"),
            Field('activity', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Add Activity')
        )

    class Meta:
        model = GroupActivityModel
        fields = '__all__'


class OrderingForm(forms.Form):
    ordering = forms.CharField()

class PartOrderingForm(forms.Form):
    ordering = forms.CharField()

class InstructionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InstructionForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.fields['activity'].widget = HiddenInput()
        self.helper.layout = Layout(
            Field('activity', css_class='form-control'),
            'pdf',
            Submit('submit', 'Add')
        )

    class Meta:
        model = instruction
        fields = '__all__'