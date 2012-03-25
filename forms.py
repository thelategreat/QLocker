
from django import forms
from django.forms import ModelForm
from models import *
from django.forms.models import fields_for_model
from django.db import models


class VariableTypesForm(forms.Form):
    variable_types_choices = VariableTypes.objects.values_list('id', 'displayname')
    print variable_types_choices
    variable_types = forms.CharField(max_length=25,
                widget=forms.Select(choices=variable_types_choices))
                

    
class VariableForm(forms.Form):
    def __init__(self, *args, **kwargs):
        variableModel = kwargs.pop('variableModel')
        super(VariableForm, self).__init__(*args, **kwargs)
        
        fields = fields_for_model(variableModel)
        print fields
        for field in fields:
            print field
            self.fields[field] = fields[field]

        
 