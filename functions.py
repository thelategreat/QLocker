###Ok, symPy just blew my mind a little, so i need to completely rethink what I'm doing here.
#Should accept a user-written string, like "<x>/<y>*60"
#Should convert this into a meaningful Python object
#Should return a pretty representation of the function
#Should be able to, given the values, substitute and solve

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
    
    
#convertStringToEquation(equationString)

