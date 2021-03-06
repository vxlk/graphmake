from util.xml import *
from util.utilities import __deprecated__

# Does the parsing from xml to node as well as all other calculations that have to do with such ...
# such as extracting and insertion of variables
class XMLConverter():
    def __init__(self):
        self.dummy = ""

    # Convert from xml node -> graphmake node
    # Used to do the automatic arg insertion as well
    # But i have since deprecated that feature
    def ConvertToNode(self, xml_node):
        nodeString = str(xml_node)
        toBeReturned = self.FillInArgs(nodeString)
        return toBeReturned

    # Convert from graphmake node to xml node
    # Will eventually undo inserted args as well
    def ConvertFromNode(self, node):
        print(str(node))
        return str(node)

    # Used to be used to auto-fill variables into appropriate slots
    def FillInArgs(self, codeString):
        __deprecated__("no longer supporting auto-fill args")
        return FillInArgs_impl(codeString)

    # Get the name of variables out of a string of code (that comes from a node)
    # these will be returned in a list without the '%' delimiters
    def GetVars(self, func_code_str):
        hasStarted = False
        skip = False
        varString = ""
        varStrings = []
        toBeReturned = func_code_str # handle multiple vars by cloning

        # parse args out of line of code
        for char in func_code_str:
            if char == '%':
                if not hasStarted:
                    hasStarted = True
                else:
                    varString += str(char)
                    hasStarted = False
                    varStrings.append(varString.replace('%', ''))
                    varString = ""
            if hasStarted:
                varString += str(char)

        return varStrings

    # eventually refactor to take a position to pick a certain var in the list
    # right now, this is instead grabbing the first var available from the list of
    # the parent given
    def ReplaceVar(self, var_str, code_str):
        return str(code_str).replace('%' + var_str + '%', FindVar(var_str))

# i should just move these into the class _impl is a bad idea here
 # for now, just pick the first one we find, will need to replace this eventually
def FindVar(name_string):
    parser = XMLUtil()
    parser.SetMode(parser.varMode)
    varString = parser.Value(name_string)
    return varString

# the auto-filling in of args is now deprecated (1/21/2021)
def FillInArgs_impl(codeString):
    return codeString
#    hasStarted = False
#    skip = False
#    varString = ""
#    varStrings = []
#    toBeReturned = codeString # handle multiple vars by cloning

    # parse args out of line of code
#    for char in codeString:
#        if char == '%':
#            if not hasStarted:
#                hasStarted = True
#            else:
#                varString += str(char)
#                hasStarted = False
#                varStrings.append(varString)
#                varString = ""
#        if hasStarted:
#            varString += str(char)

#    # find and replace var holders with the actual vars
#    for var in varStrings:
#        varStringNoDelimiter = var.replace('%', '')
#        actualVar = FindVar(varStringNoDelimiter)
#        logger.Log("actual variable: " + actualVar)
#        toBeReturned = toBeReturned.replace(var, actualVar)
#        logger.Log("code string: " + toBeReturned)
#    logger.Log(toBeReturned + " <- with args filled in")
#    return toBeReturned
