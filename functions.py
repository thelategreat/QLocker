

#I hate import *
from sympy import *



def declareVariables(equationString):
    #TODO make this a regular expression
    variables = equationString.split("<")
    variableList = []
    for variableChunk in variables[1:]:
        variable = variableChunk.split(">")[0]
        variableList += [variable]
    for variable in variableList:
        
        print "%s = Symbol('%s')" % (variable, variable)
        exec "%s = Symbol('%s')" % (variable, variable)
    #remove variable indicators
    equationString=equationString.replace("<",'').replace(">","")
    print equationString
    return equationString
    
    
    
def convertStringToEquation(equationString):
    #Declare our variables
    equationString = declareVariables(equationString)
    exp = S(equationString)
    return latex(exp)

    
def convertStringToFunction(equationString):
    #Declare our variables
    equationString = declareVariables(equationString)
    exp = S(equationString)
    return exp
    
def solveFunction(function, variables):
    for v in variables.keys():
        function = function.subs(v, variables[v])
    return function
    
#convertStringToEquation(equationString)

