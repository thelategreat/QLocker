from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.template import Context, RequestContext
from models import *
from forms import *
import functions

class editorView(TemplateView):
    template_name = 'editor.html'

    def get_context_data(self, **kwargs):
        equationString = "(cos(<x>^2)/<y>)*60"
        latexString = functions.convertStringToEquation(equationString)
        variable_types = VariableTypes.objects
        #print VariableTypes.objects.values('id', 'description')
        variable_types_form = VariableTypesForm()
        ctx = {
                'latexString':latexString,
                'variable_types_form':variable_types_form,
                }
        return ctx
        
        
class ajaxEquationView(TemplateView):
    template_name = "ajaxEquation.html"

    
    def get_context_data(self, **kwargs):
        #context = super(ajaxEquationView, self).get(self, request, *args, **kwargs)
        print "hi"
        equationString = self.request.GET.get('e', '')
        #equationString = "(cos(<x>^2)/<y>)*60"
        latexString = functions.convertStringToEquation(equationString)
        #print context
        ctx = {'latexString':latexString}
        return ctx
        
class variableAttributesView(TemplateView):
    template_name = "variableAttributes.html"
    
    def get_context_data(self, **kwargs):
        print self.request.GET
        variableKey = self.request.GET.get('type', 1)
        variableClassString = VariableTypes.objects.filter(id = variableKey).values('classname')[0]['classname']
        print variableClassString
        exec("variableModel = "+variableClassString+"()")
        print variableModel
        variablesForm = VariableForm(variableModel = variableModel)
        ctx = {
                'variablesForm':variablesForm,
                }
        return ctx
        
class saveVariableAttributesView(TemplateView):
    template_name = "variableAttributes.html"
    
    def get_context_data(self, **kwargs):
        print self.request.GET
        var = IntegerRange()
        var.load_values(self.request.GET)
        var.save_it()
        return
        
    