from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.template import Context, RequestContext
from models import *
from forms import *
import functions
import json
from django.db.models import Q
import re

class editorView(TemplateView):
    template_name = 'editor.html'

    def get_context_data(self, **kwargs):
        equationString = "(cos(<x>^2)/<y>)*60"
        latexString = functions.convertStringToEquation(equationString)
        variable_types = VariableTypes.objects
        #print VariableTypes.objects.values('id', 'description')
        variable_types_form = VariableTypesForm()
        questionsForm = QuestionsForm()
        ctx = {
                'latexString':latexString,
                'variable_types_form':variable_types_form,
                'questionsForm':questionsForm,
                }
        return ctx
        
        
class ajaxEquationView(TemplateView):
    template_name = "ajaxEquation.html"

    
    def get_context_data(self, **kwargs):
        #context = super(ajaxEquationView, self).get(self, request, *args, **kwargs)
        #print "hi"
        equationString = self.request.GET.get('e', '')
        #equationString = "(cos(<x>^2)/<y>)*60"
        latexString = functions.convertStringToEquation(equationString)
        #print context
        ctx = {'latexString':latexString}
        return ctx
        
class variableAttributesView(TemplateView):
    template_name = "variableAttributes.html"
    
    def get_context_data(self, **kwargs):
        #See if the variable exists
        displayName = self.request.GET.get('displayname',None)
        force = self.request.GET.get('force', "false")
        #variable_id = int(self.request.GET.get('variable_id', '0'))
        
        existingVariables = Variable.objects.filter(Q(displayname = displayName)).values()
        variableKey = self.request.GET.get('type', 1)
        if existingVariables.count() > 0:
            print "Found!"
            existingVariable = existingVariables[0]
            if force == "false":
                variableKey = existingVariable.get('variable_types', 1)              
        else:
            existingVariable = {}
        print "Key: ", variableKey
        variableClassString = VariableTypes.objects.filter(id = variableKey).values('classname')[0]['classname']
        exec("variableModel = "+variableClassString+"()")
        variablesForm = VariableForm(variableModel = variableModel, existingVariable =  existingVariable)
        variable_types_form = VariableTypesForm(initial={'variable_types':variableKey})
        
        ctx = {
                'variablesForm':variablesForm,
                'variable_types_form':variable_types_form,
                }
        return ctx
        
class saveVariableAttributesView(TemplateView):
    template_name = "variableAttributes.html"
    
    def get_context_data(self, **kwargs):
        variableKey = self.request.GET.get('variable_types', 1)
        variableClassString = VariableTypes.objects.filter(id = variableKey).values('classname')[0]['classname']
        print variableClassString
        exec("variableModel = "+variableClassString+"()")
        variableModel.load_values(self.request.GET)
        variableModel.save_it()
        return
        
class saveQuestionView(TemplateView):
    template_name = "jsonResponse.html"
    
    def get_context_data(self, **kwargs):
        print self.request.GET
        question = self.request.GET.get('question',None)
        solution = self.request.GET.get('solution',None)
        id = self.request.GET.get('id','0')
        #save question
        questionAttributes = Questions()
        id = int(id)
        if id != 0:
            questionAttributes.id = id
        questionAttributes.question = question
        questionAttributes.solution = solution
        questionAttributes.save()
        #return key
        response = {'question_id':questionAttributes.id}
        jsonResponse = json.dumps(response)
        
        ctx = {
                'jsonResponse' : jsonResponse,
                }
        return ctx
        
class generateVariableView(TemplateView):
    template_name = "jsonResponse.html"
    
    def get_context_data(self, **kwargs):
        print self.request.GET
        value = None
        variable_id = int(self.request.GET.get('variable_id', '0'))
        if variable_id > 0:
            value = self.getValue(variable_id)
            #jsonResponse = json.dumps(existingVariable.values())
        jsonResponse = value
        ctx = {
                'jsonResponse' : jsonResponse,
                }
        return ctx
        
    def getValue(self, variable_id):
        existingVariables = Variable.objects.filter(Q(id = variable_id)).values()
        if existingVariables.count() > 0:
            existingVariable = existingVariables[0]
            variableClassString = existingVariable['classname']
            print variableClassString
            exec("variableModel = "+variableClassString+"()")
            variableModel.load_values(json.loads(existingVariable['attributes']))
            value = variableModel.generate()
            return value
            
    def getValueFromName(self, name):
        existingVariables = Variable.objects.filter(Q(displayname = name)).values()
        if existingVariables.count() > 0:
            existingVariable = existingVariables[0]
            variableClassString = existingVariable['classname']
            print variableClassString
            exec("variableModel = "+variableClassString+"()")
            variableModel.load_values(json.loads(existingVariable['attributes']))
            value = variableModel.generate()
            return value
        
class generateQuestionView(TemplateView):
    template_name = "jsonResponse.html"
    
    def get_context_data(self, **kwargs):
        value = None
        question_id = int(self.request.GET.get('question_id', '0'))
        jsonResponse = None
        if question_id > 0:
            existingQuestions = Questions.objects.filter(Q(id = question_id))
            if existingQuestions.count() > 0:
                question = existingQuestions[0]
                values = question.generateValues()
                displayQuestion = question.createDisplayQuestion()
                answer =  str(question.solveSolution())
                response = {
                            'displayQuestion':displayQuestion,
                            'answer':answer,
                            }
                jsonResponse = json.dumps(response)
       
        ctx = {
                'jsonResponse' : jsonResponse,
                }
        return ctx
        

        
        