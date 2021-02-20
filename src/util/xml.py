import xml.etree.ElementTree as ET
from util.settings import *
from util.logger import *
from util.utilities import __deprecated__
from util.level_list import *

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
        self.invalid_node = ""
        
    # Use the settings object to open the appropriate db
    # FOR NOW THESE STAY OPEN FOR THE LIFETIME OF THE PROJECT
    # TODO: PROPERLY HANDLE YOUR IO AND CLOSE THESE THINGS
    def OpenFile(self):
        if self.modeVar is True:
            return settings.varPath
        else:
            return settings.dbPath
    
    # Given the name of the new document/db (use the given variables for the names so you don't mess up)
    # switch our view to the new document/db
    def SetMode(self, modeStr):
        if modeStr == self.funcMode:
            self.modeVar = False
            self.modeFunc = True
        elif modeStr == self.varMode:
            self.modeVar = True
            self.modeFunc = False

    # Return the string name of the database we are currently looking at
    def Mode(self):
        if self.modeFunc == True:
            return self.funcMode
        else:
            return self.varMode

    # If in var mode -> func mode
    # If in func mode -> var mode
    def FlipMode(self):
        if self.modeFunc == True:
            self.modeFunc = False
            self.modeVar = True
        else:
            self.modeFunc = True
            self.modeVar = False

    # Root of the current document (node not name/string)
    def Root(self):
        file = self.OpenFile()
        root = ET.parse(file).getroot()       
        return root

    # Name of the root of the current document
    def RootName(self):
        root_node = Root()
        return root_node.tag

    # returns the name of the parent node of the given child's name right below the root
    # the "parent below the root"
    # put your result variable in the result_str column
    def ParentBelowRoot(self, name_string_searched_for):
        # __deprecated__("I am reworking this, i want to come back to it later - when the database beautifying phase goes into effect")
        level_list = LevelList()
        self.LevelList(level_list)
        found_node = level_list.FindNode(name_string_searched_for)
        if found_node == None:
            return ""
        else:
            # get the highest level parent'
            parent_name = ""
            node_parent = found_node.Up()
            while node_parent != None:
                parent_name = node_parent.Data()
                node_parent = node_parent.Up()
            return parent_name
       
    # generator function to recursive find
    #def find_rec(self, node, element):
    #   for item in node.findall(element):
    #        yield item
    #    for child in self.find_rec(item, element):
    #        yield child

    # recursive find of a node ... does not include attributes
    def find_rec(self, node, element, result):
        for item in node.findall(element):
            result.append(item)
            self.find_rec(item, element, result)
        return result

    # get all children of a given node
    def find_children_rec(self, node, result):
        for child in node:
            result.append(child)
            self.find_children_rec(child, result)
        return result

    # find nodes that contain a certain attribute
    def find_nodes_with_attrib(self, node_root, attr_name_str, result):
        for child in node_root:
            if child.tag == attr_name_str:
                result.append(child)
            for attrib in child.attrib:
                if attrib == attr_name_str:
                    result.append(child)
            self.find_nodes_with_attrib(child, attr_name_str, result)

    # return true if a node has children
    def has_children(self, node):
        # debug code included
        child_list = list(node)
        logger.Log("list of children:")
        logger.Log(child_list)
        return len(node) != 0

    def has_attrib(self, node):
        attrib_list = list(node.attrib)
        return len(attrib_list) != 0 

    # Gets the value of 
    def Value(self, tag):
        toBeReturned = ""
        toBeReturned = self.FindNode_impl(tag)
        # needs to be reworked ... check the other database if no match
        if (toBeReturned == ""):
            self.FlipMode()
            toBeReturned = self.FindNode_impl(tag)
        return toBeReturned

    # Given the value, get the name of the attribute assigned to it
    def ValueName(self, tag):
        toBeReturned = ""
        toBeReturned = self.FindNodeReverse_impl(tag)
        # needs to be reworked ... check the other database if no match
        if (toBeReturned == ""):
            self.FlipMode()
            toBeReturned = self.FindNodeReverse_impl(tag)
        return toBeReturned

    # implementation of find node, should not be called directly
    # but is called by utility functions provided by this class
    def FindNode_impl(self, tag):   
        root = self.Root()
        logger.Log("mode: " + self.Mode())
        logger.Log("root " + str(root))
        
        _list = []
        logger.Log("looking for tag: " + tag)
        self.find_nodes_with_attrib(root, tag, _list)

        logger.Log("parent list: " + str(_list))

        returnedList = []
        for item in _list:
            if (self.has_children(item)):
                logger.Log("I have children : " + str(item))
                childList = []
                self.find_children_rec(item, childList)
                for child in childList:
                    for attrib in child.attrib:
                        logger.Log("Tag: " + str(item.tag))
                        strAttrib = str(child.get(attrib))
                        logger.Log("Attrib: " + strAttrib)
                        returnedList.append(strAttrib)
            else:
                logger.Log("I have no children : " + str(item))
                for attrib in item.attrib:
                    strAttrib = str(item.get(attrib))
                    if attrib == tag:
                        returnedList.append(strAttrib)

        # return the first for now, only temporary
        if len(returnedList) > 0:
            return returnedList[0]

        # not found
        return ""

    def FindNodeReverse_impl(self, tag):
        root = self.Root()
        logger.Log("mode: " + self.Mode())
        logger.Log("root " + str(root))
        
        # search the entire database - we can't narrow the search here
        _list = [] 
        self.find_children_rec(root, _list)
        logger.Log("looking for tag: " + tag)

        logger.Log("parent list: " + str(_list))

        returnedList = []
        for item in _list:
            if (self.has_children(item)):
                logger.Log("I have children : " + str(item))
                childList = []
                self.find_children_rec(item, childList)
                for child in childList:
                    for attrib in child.attrib:
                        # get values
                        if child.get(attrib) == tag or child.tag == tag:
                            returnedList.append(attrib)
            else:
                logger.Log("I have no children : " + str(item))
                for attrib in item.attrib:
                    # get values
                    if attrib == tag or item.tag == tag:
                        returnedList.append(attrib)

        # return the first for now, only temporary
        if len(returnedList) > 0:
            return returnedList[0]

        # not found
        return ""

    # Get the "code" associated with a certain node if it exists
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
            child_array = []
            self.find_children_rec(child, child_array)
            # todo: handle tags better
            str_names.append(child.tag)

            for attrib in child.attrib:
                str_names.append(attrib)

            for childs_child in child_array:
                str_names.append(childs_child.tag)
                for attrib in childs_child.attrib:
                    str_names.append(attrib)
                    
        return str_names

    # Builds a level list (dictionary of ints corresponding to level in tree) with name
    # of node
    def LevelList(self, level_list_structure_out, int_level = 0, node = None):
        level = int_level
        if (node is None):
            node = self.Root()
       
        for child in node:
            level_list_structure_out.AddNode(child.tag, int_level)
   
            attrib_level = int_level
            if self.has_attrib(child):
                attrib_level += 1
                for attrib in child.attrib:
                    level_list_structure_out.AddNode(attrib, attrib_level)

            if self.has_children(node):
                level = int_level + 1
            self.LevelList(level_list_structure_out, level, child)

    # all attribs from a node of given name str_node_name
    def AttributesForNodeName(self, str_node_name):
        logger.Log("All Attributes for node " + str(str_node_name), __name__)
        self.SetMode(self.funcMode)
        values = Values(str_node_name)
        for value in values:
            logger.Log(str(value.tag))
        return Values(str_node_name)