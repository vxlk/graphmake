import xml.etree.ElementTree as ET
from util.settings import *
from util.logger import *

# handles reading of xml, also handles opening the correct file,
# the responsibility of setting the correct file is that of the 
# database's

class XMLUtil():
    def __init__(self):
        # this will need revisiting with scale ... fine for now
        self.funcMode = "Function"
        self.varMode = "Var"
        self.modeVar = False
        self.modeFunc = True

    def OpenFile(self):
        if self.modeVar is True:
            return settings.varPath
        else:
            return settings.dbPath
    
    def SetMode(self, modeStr):
        if modeStr == self.funcMode:
            self.modeVar = False
            self.modeFunc = True
        elif modeStr == self.varMode:
            self.modeVar = True
            self.modeFunc = False

    def Root(self):
        file = self.OpenFile()
        root = ET.parse(file).getroot()       
        return root

    # generator function to recursive find
    #def find_rec(self, node, element):
    #   for item in node.findall(element):
    #        yield item
    #    for child in self.find_rec(item, element):
    #        yield child

    def find_rec(self, node, element, result):
        for item in node.findall(element):
            result.append(item)
            self.find_rec(item, element, result)
        return result

    def Value(self, tag):
        root = self.Root()
        
        logger.Log("root " + str(root))
        
        _list = []
        self.find_rec(root, tag, _list)

        logger.Log(str(_list))

        returnedList = []
        for item in _list:
            for attrib in item.attrib:
                logger.Log("Tag: ")
                logger.Log(str(item.tag))
                strAttrib = str(item.get(attrib))
                logger.Log("Attrib: ")
                logger.Log(strAttrib)
                returnedList.append(strAttrib)
        # return the first for now, only temporary
        if len(returnedList) > 0:
            return returnedList[0]
        return ""

    def Values(self, tag):
        root = self.Root()
        
        _list = []
        self.find_rec(root, tag, _list)

        returnedList = []
        for item in _list:
            for attrib in item.attrib:
                strAttrib = str(item.get(attrib))
                returnedList.append(strAttrib)
        # return the first for now, only temporary
        if len(returnedList) > 0:
            return returnedList
        return []

    def AllNodeNames(self):
        self.SetMode(self.funcMode)
        root = self.Root()
        str_names = []
        for child in root:
            str_names.append(child.tag)
        return str_names

    def AttributesForNodeName(self, str_node_name):
        logger.Log("All Attributes for node " + str(str_node_name), __name__)
        self.SetMode(self.funcMode)
        values = Values(str_node_name)
        for value in values:
            logger.Log(str(value.tag))
        return Values(str_node_name)