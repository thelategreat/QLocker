from django.db import models
import json

class VariableTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    displayname = models.CharField(max_length=135, db_column='displayName', blank=True) # Field name made lowercase.
    classname = models.CharField(max_length=135, db_column='className', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=450, blank=True)
    class Meta:
        db_table = u'variable_types'
    
class IntegerRange(models.Model):
    id = models.IntegerField(primary_key=True)
    displayname = models.CharField(max_length=135, db_column='displayName', blank=True)
    start = models.IntegerField()
    stop = models.IntegerField()
    step = models.IntegerField()
    
    def load_values(self, get_vars):
        self.displayname = get_vars.get("displayname", "None")
        self.start = get_vars.get("start", 1)
        self.stop = get_vars.get("stop",10)
        self.step = get_vars.get("step",1)
    
    def save_it(self):
        variableModel = Variable()
        variableModel.displayname = self.displayname
        variableModel.attributes = json.dumps({"start":self.start, "stop":self.stop, "step":self.step})
        variableModel.save()
    
class DefinedSet(models.Model):
    id = models.IntegerField(primary_key=True)
    displayname = models.CharField(max_length=135, db_column='displayName', blank=True)
    values = models.CharField()

    
    def load_values(self, get_vars):
        self.displayname = get_vars.get("displayname", "None")
        self.start = get_vars.get("start", 1)
        self.stop = get_vars.get("stop",10)
        self.step = get_vars.get("step",1)
    
    def save_it(self):
        variableModel = Variable()
        variableModel.displayname = self.displayname
        variableModel.attributes = json.dumps({"start":self.start, "stop":self.stop, "step":self.step})
        variableModel.save()

    
class Variable(models.Model):
    id = models.IntegerField(primary_key=True)
    displayname = models.CharField(max_length=135, db_column='displayName', blank=True)
    attributes = models.TextField(blank=True)
    
    class Meta:
        db_table = u'variables'
    
