import xml.etree.ElementTree as ET
from util.settings import *
from util.logger import *
from util.utilities import __deprecated__

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
        self.string_result = "" # used by functions that need to store a string result 
                                # (only promised to be valid after an operation that sets it)

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

    def Mode(self):
        if self.modeFunc == True:
            return self.funcMode
        else:
            return self.varMode

    def FlipMode(self):
        if self.modeFunc == True:
            self.modeFunc = False
            self.modeVar = True
        else:
            self.modeFunc = True
            self.modeVar = False

    def Root(self):
        file = self.OpenFile()
        root = ET.parse(file).getroot()       
        return root

    def RootName(self):
        root_node = Root()
        return root_node.tag

    # returns the name of the parent node of the given child's name right below the root
    # the "parent below the root"
    # put your result variable in the result_str column
    def ParentBelowRoot(self, name_string_searched_for, result_str, traversal_list_private = [], node_private = None, found = False):
        __deprecated__("I am reworking this, i want to come back to it later - when the database beautifying phase goes into effect")
        
        #if node_private == None:
        #    node_private = self.Root()
        ## check nodes
        #for child in node_private:
        #    # found root
        #    if child.tag == name_string_searched_for:
        #        # return highest child
        #        if len(traversal_list_private) > 0:
        #            result_str = traversal_list_private[0]
        #            found = True
        #        # parent is root
        #        else:
        #            result_str = self.Root().tag
        #            found = True
        #    # check attributes on the node
        #    for attrib in child.attrib:
        #        # found root
        #        if attrib == name_string_searched_for:
        #            # return highest child
        #            if len(traversal_list_private) > 0:
        #                result_str = traversal_list_private[0]
        #                found = True
        #            # parent is root
        #            else:
        #                result_str = self.Root().tag
        #                found = True

        #    traversal_list_private.append(child.tag)
        #    if (found == False):
        #        self.ParentBelowRoot(name_string_searched_for, result_str, traversal_list_private, child)

    def ParentBelowRootSuckWay(self, name_string_searched_for, node_private = None, found = False):
        __deprecated__("this sucks, change it")
        if node_private == None:
            node_private = self.Root()
        # check nodes
        for child in node_private:
            # check attributes on the node
            for attrib in child.attrib:
                # found
                if attrib == name_string_searched_for:
                    found = True
                    self.string_result = child.attrib['Parent']
              
            if (found == False):
                self.ParentBelowRootSuckWay(name_string_searched_for, child, found)

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

    def find_children_rec(self, node, result):
        for child in node:
            result.append(child)
            self.find_children_rec(child, result)
        return result

    def find_nodes_with_attrib(self, node_root, attr_name_str, result):
        for child in node_root:
            if child.tag == attr_name_str:
                result.append(child)
            for attrib in child.attrib:
                if attrib == attr_name_str:
                    result.append(child)
            self.find_nodes_with_attrib(child, attr_name_str, result)

    def has_children(self, node):
        # debug code included
        child_list = list(node)
        logger.Log("list of children:")
        logger.Log(child_list)
        return len(node) != 0

    def has_attrib(self, node):
        attrib_list = list(node.attrib)
        return len(attrib_list) != 0 

    def Value(self, tag):
        toBeReturned = ""
        toBeReturned = self.FindNode_impl(tag)
        # needs to be reworked ... check the other database if no match
        if (toBeReturned == ""):
            self.FlipMode()
            toBeReturned = self.FindNode_impl(tag)
        return toBeReturned

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


    def LevelList(self, level_list_dict, int_level = 0, node = None):
        if (node is None):
            node = self.Root()
        for child in node:
            level = int_level + 1
            level_list_dict[child.tag] = level
            self.LevelList(level_list_dict, level, child)

            if self.has_attrib(child):
                level += 1
                for attrib in child.attrib:
                    level_list_dict[attrib] = level

    def AttributesForNodeName(self, str_node_name):
        logger.Log("All Attributes for node " + str(str_node_name), __name__)
        self.SetMode(self.funcMode)
        values = Values(str_node_name)
        for value in values:
            logger.Log(str(value.tag))
        return Values(str_node_name)