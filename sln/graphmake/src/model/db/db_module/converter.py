from util.xml import *

# Does the parsing from xml to node
class XMLConverter():
    def __init__(self):
        self.dummy = ""

    def ConvertToNode(self, node):
        logger.Log(node)
        nodeString = str(node)
        logger.Log(nodeString + "<- before args")
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
    varStrings = []
    toBeReturned = codeString # handle multiple vars by cloning

    # parse args out of line of code
    for char in codeString:
        if char == '%':
            if not hasStarted:
                hasStarted = True
            else:
                varString += str(char)
                hasStarted = False
                varStrings.append(varString)
                varString = ""
        if hasStarted:
            varString += str(char)

    # find and replace var holders with the actual vars
    for var in varStrings:
        varStringNoDelimiter = var.replace('%', '')
        actualVar = FindVar(varStringNoDelimiter)
        logger.Log("actual variable: " + actualVar)
        toBeReturned = toBeReturned.replace(var, actualVar)
        logger.Log("code string: " + toBeReturned)
    logger.Log(toBeReturned + " <- with args filled in")
    return toBeReturned
