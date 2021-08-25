from django import forms
from django.forms import HiddenInput

from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Div, Submit, HTML, Hidden, Row, Column, Field, Button


# from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class PartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'obsolete',
            Field('partNumber', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('location', css_class='form-control'),
            Row(
                Column(
                    Div(
                        Field('stockOnHand', css_class='form-control', required=True,),

                        Button('add stock', '+ / -', css_class="btn btn-success h-50 align-self-center"),

                        css_class="input-group-append"),
                    css_class='input-group col-md-3'),
                Column(
                    Field('minimumStock', css_class='form-control', required=True),
                    css_class='col-md-2'
                ),
                Column(
                    Field('reorderQtys', css_class='form-control', required=True),
                    css_class='col-md-2'
                ),
                css_class='row justify-content-between form-row'
            ),
            Field('leadtime', css_class='form-control'),
            Row(
                Column(
                    Field('boxSize', css_class='form-control', required=True),
                    css_class='col-md-6'
                ),
                Column(
                    Field('weight', css_class='form-control', required=True),
                    css_class='col-md-6'
                ),
                css_class='form-row form_group'
            ),
            Field('group', css_class='form-control', disabled=True),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = PartModel
        fields = '__all__'

class LowStockGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LowStockGroupForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('partNumber', type='hidden'),
            Field('group', css_class='form-control'),
            Submit('submit', 'Add Group')
        )

    class Meta:
        model = PartModel
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('supplierName', css_class='form-control'),
            HTML('<br>'),
            Submit('save', 'Save')
        )

    class Meta:
        model = SupplierModel
        fields = '__all__'


class PartCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartCommentForm, self).__init__(*args, **kwargs)

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
        model = PartCommentModel
        fields = ['comment', 'author', 'part']


class PartSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartSupplierForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('supplierPartNumber', css_class='form-control'),
            Field('part', type='hidden'),
            Field('supplier', css_class='form-control'),
            'preferred',
            Submit('submit', 'Add Supplier')
        )

    class Meta:
        model = PartSupplierModel
        fields = '__all__'


class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.fields['part'].widget = HiddenInput()
        self.helper.layout = Layout(
            Field('part', css_class='form-control'),
            'image',
            Submit('submit', 'Add')
        )

    class Meta:
        model = PartImageModel
        fields = '__all__'
