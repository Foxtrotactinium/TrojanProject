from django import forms
from .models import PartsList, Suppliers, PartComments
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Div, Submit, HTML, Hidden, Row, Column, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


#


class part_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(part_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('partnumber', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('location', css_class='form-control'),
            Row(
                Column(
                    Field('stockonhand', css_class='form-control mb-0'),
                    css_class='col-md-4'
                ),
                Column(
                    Field('minimumstock', css_class='form-control mb-0'),
                    css_class='col-md-4'
                ),
                Column(
                    Field('reorderqtys', css_class='form-control mb-0'),
                    css_class='col-md-4'
                ),
                css_class='form-row'
            ),
            Field('leadtime', css_class='form-control'),
            Row(
                Column(
                    Field('boxsize', css_class='form-control mb-0'),
                    css_class='col-md-6'
                ),
                Column(
                    Field('weight', css_class='form-control mb-0'),
                    css_class='col-md-6'
                ),
                css_class='form-row form_group'
            ),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = PartsList
        fields = '__all__'


class supplier_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(supplier_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('supplier', css_class='form-control'),
            Field('phonenumber', css_class='form-control'),
            Field('address', css_class='form-control'),
            Field('customeraccountnumber', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = Suppliers
        fields = '__all__'


class part_comment_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(part_comment_form, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('comment', css_class='form-control', rows="2"),
            Field('author', type='hidden'),
            Field('part', type='hidden'),
            Submit('submit', 'Add Comment')
        )

    class Meta:
        model = PartComments
        fields = ['comment', 'author', 'part']
