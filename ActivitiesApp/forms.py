from django import forms
from .models import ActivityModel, ActivityPartModel, GroupModel, GroupActivityModel
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
            Field('increment', type='hidden'),
            HTML('<br>'),
            Submit('save', 'Save')
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
            'workCenter',
            Submit('save', 'Save')
        )

    class Meta:
        model = GroupModel
        fields = ['groupName', 'workCenter']


class required_activity_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(required_activity_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('group', type="hidden"),
            Field('activity', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = GroupActivityModel
        fields = '__all__'
#
#
# class TypesForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(TypesForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.layout = Layout('workCenter')
#
#     class Meta:
#         model = GroupModel
#         fields = ['workCenter']