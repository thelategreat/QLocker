from django.db import models
import json
import traceback
from django.db.models import Q 
import random
import functions
import re



class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    variables = {}
    displayQuestion = ""
    solutionValue = 0
    class Meta:
        db_table = u'questions'
        
    def generateValues(self):
        self.variables = {}
        for v in re.findall(r'<([^>]+)>', self.question+ " " + self.solution):
            variable = Variable().loadByName(v)
            value = variable.getValue()
            self.variables.setdefault(v, value)
        return self.variables
        
    def createDisplayQuestion(self): 
        self.displayQuestion = self.question
        for value in self.variables.keys():
            self.displayQuestion = self.displayQuestion.replace("<"+value+">",str(self.variables[value]) )
        return self.displayQuestion
        
    def solveSolution(self):
        f=functions.convertStringToFunction(self.solution)
        self.solutionValue = functions.solveFunction(f, self.variables)
        return self.solutionValue

class VariableTypes(models.Model):
    id = models.AutoField(primary_key=True)
    displayname = models.CharField(max_length=135, db_column='displayName', blank=True) # Field name made lowercase.
    classname = models.CharField(max_length=135, db_column='className', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=450, blank=True)
    class Meta:
        db_table = u'variable_types'
    
class IntegerRange(models.Model):
    className = "IntegerRange"
    id = models.IntegerField(primary_key=True, editable=False)
    displayname = models.CharField(max_length=135, db_column='displayName', blank=True)
    variable_types = models.IntegerField()
    start = models.IntegerField()
    stop = models.IntegerField()
    step = models.IntegerField()
    
    def load_values(self, get_vars):
        print get_vars
        self.displayname = get_vars.get("displayname", "None")
        self.start = get_vars.get("start", 1)
        self.stop = get_vars.get("stop",10)
        self.step = get_vars.get("step",1)
        self.variable_types = get_vars.get("variable_types",1)
        
    
    def save_it(self):
        variableModel = Variable()
        variableModel.displayname = self.displayname
        variableModel.variable_types = self.variable_types
        traceback.print_exc()
        variableModel.attributes = json.dumps({"start":self.start, "stop":self.stop, "step":self.step})
        variableModel.classname = "IntegerRange"
        #print variableModel
        variableModel.save_it()
        
    def generate(self):
        value = random.randrange(int(self.start), int(self.stop), int(self.step))
        return value
    
class DefinedSet(models.Model):
    className = "DefinedSet"
    id = models.IntegerField(primary_key=True, editable=False)
    displayname = models.CharField(max_length=135, db_column='displayName', blank=True)
    variable_types = models.IntegerField()
    values = models.CharField()

    
    def load_values(self, get_vars):
        self.displayname = get_vars.get("displayname", "None")
        self.variable_types = get_vars.get("variable_types",1)
        self.values = get_vars.get("values", "0")


        
    
    def save_it(self):
        variableModel = Variable()
        variableModel.displayname = self.displayname
        variableModel.variable_types = self.variable_types
        variableModel.attributes = json.dumps({"values":self.values})
        variableModel.classname = "DefinedSet"
        print variableModel.variable_types
        variableModel.save_it()
    
class Variable(models.Model):
    id = models.IntegerField(primary_key=True)
    displayname = models.CharField(max_length=135, db_column='displayName', blank=True)
    variable_types = models.IntegerField()
    attributes = models.TextField(blank=True)
    classname = models.CharField(max_length=135)
    
    def save_it(self):
        existingVariables = Variable.objects.filter(Q(displayname = self.displayname))
        if (existingVariables.count() > 0):
            existingVariable = existingVariables[0]
            existingVariable.variable_types = self.variable_types
            existingVariable.attributes = self.attributes
            existingVariable.classname = self.classname
            existingVariable.save()
        else:
            self.save()

    def loadById(self, id):
        variable = None
        variables = Variable.objects.filter(Q(id = id))
        if variables.count() > 0:
            variable = variable[0]
        return variable
        
    def loadByName(self, name):
        variable = None
        variables = Variable.objects.filter(Q(displayname = name))
        if variables.count() > 0:
            variable = variables[0]
        return variable
        
    def getValue(self):
            variableClassString = self.classname
            print variableClassString
            exec("variableModel = "+variableClassString+"()")
            variableModel.load_values(json.loads(self.attributes))
            value = variableModel.generate()
            return value
        
        
    class Meta:
        db_table = u'variables'
    
