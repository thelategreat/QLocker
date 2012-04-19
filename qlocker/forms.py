 
from django import forms
from django.forms import ModelForm
from models import *
from django.forms.models import fields_for_model
from django.db import models
import json
from django.forms import widgets


class VariableTypesForm(forms.Form):
    variable_types_choices = VariableTypes.objects.values_list('id', 'displayname')
    #print "choices: ", variable_types_choices
    variable_types = forms.CharField(max_length=25,
                widget=forms.Select(choices=variable_types_choices))
                

class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        
                
    
class VariableForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        variableModel = kwargs.pop('variableModel')
        initial = kwargs.pop('existingVariable', {})
        attributesString = initial.get('attributes', "{}")
        attributes = json.loads(attributesString)
        #print attributes
        super(VariableForm, self).__init__(*args, **kwargs)
        self.type = variableModel.className
        fields = fields_for_model(variableModel)
        #print fields
        self.fields['className'] = forms.CharField(max_length=25, widget=forms.HiddenInput(), initial=variableModel.className)
        for field in fields:
            self.fields[field] = fields[field]
            self.fields[field].initial = attributes.get(field, None)
        self.fields['displayname'] = forms.CharField(max_length=25, widget=forms.HiddenInput())
        self.fields.pop('variable_types')
        
 