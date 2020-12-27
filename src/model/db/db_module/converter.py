from util.xml import *

# Does the parsing from xml to node
class XMLConverter():
    def __init__(self):
        self.dummy = ""

    def ConvertToNode(self, node):
        nodeString = str(node)
        toBeReturned = self.FillInArgs(nodeString)
        return toBeReturned

    def ConvertFromNode(self, node):
        print(str(node))
        return str(node)

    def FillInArgs(self, codeString):
        return FillInArgs_impl(codeString)


# i should just move these into the class _impl is a bad idea here
 # for now, just pick the first one we find, will need to replace this eventually
def FindVar(name_string):
    parser = XMLUtil()
    parser.SetMode(parser.varMode)
    varString = parser.Value(name_string)
    return varString

def FillInArgs_impl(codeString):
    hasStarted = False
    skip = False
    varString = ""
    for char in codeString:
        if char == '%':
            if not hasStarted:
                hasStarted = True
            else:
                varString += str(char)
                hasStarted = False
        if hasStarted:
            varString += str(char)
    varStringNoDelimiter = varString.replace('%', '')
    actualVar = FindVar(varStringNoDelimiter)
    toBeReturned = codeString.replace(varString, actualVar)
    return toBeReturned
