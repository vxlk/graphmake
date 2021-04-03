import xml.etree.ElementTree as ET
from util.settings import *
from util.logger import *
from util.utilities import __deprecated__
from util.level_list import *

class DBMode():
    functionMode = "Function Mode"
    variableMode = "Variable Mode"
    descriptionMode = "Description Mode"
    tagMode = "Tag Mode"

# handles reading of xml, also handles opening the correct file,
# the responsibility of setting the correct file is that of the 
# database's
class XMLUtil():
    def __init__(self):
        # this will need revisiting with scale ... fine for now
        self.current_mode = DBMode.functionMode
        self.invalid_node = ""
        
    # Use the settings object to open the appropriate db
    def GetDBPath(self) -> str:
        if self.current_mode == DBMode.variableMode:
            return settings.varPath
        if self.current_mode == DBMode.functionMode:
            return settings.dbPath
        if self.current_mode == DBMode.descriptionMode:
            return settings.descPath
        if self.current_mode == DBMode.tagMode:
            return settings.tagPath
    
    # Root of the current document (node not name/string)
    def Root(self) -> ET.Element:
        if (self.current_mode == 1):
            x = 1
        print(self.current_mode)
        file = self.GetDBPath()
        print(file)
        root = ET.parse(file).getroot()       
        return root

    # Name of the root of the current document
    def RootName(self) -> str:
        root_node = Root()
        return root_node.tag

    def SetMode(self, mode : str) -> None:
        self.current_mode = mode

    def FlipMode(self) -> None:
        if (self.current_mode == DBMode.functionMode):
            self.current_mode = DBMode.variableMode
        if (self.current_mode == DBMode.variableMode):
            self.current_mode = DBMode.functionMode

    # returns the name of the parent node of the given child's name right below the root
    # the "parent below the root"
    # put your result variable in the result_str column
    def ParentBelowRoot(self, name_string_searched_for : str) -> str:
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
    def find_rec(self, node : ET.Element, element : str, result : list) -> list:
        for item in node.findall(element):
            result.append(item)
            self.find_rec(item, element, result)
        return result

    # get all children of a given node
    def find_children_rec(self, node : ET.Element, result : list) -> list:
        for child in node:
            result.append(child)
            self.find_children_rec(child, result)
        return result

    # find nodes that contain a certain attribute
    def find_nodes_with_attrib(self, node_root : ET.Element, attr_name_str : str, result : list) -> None:
        for child in node_root:
            if child.tag == attr_name_str:
                result.append(child)
            for attrib in child.attrib:
                if attrib == attr_name_str:
                    result.append(child)
            self.find_nodes_with_attrib(child, attr_name_str, result)

    # return true if a node has children
    def has_children(self, node : ET.Element) -> bool:
        # debug code included
        child_list = list(node)
        return len(node) != 0

    def has_attrib(self, node : ET.Element) -> bool:
        attrib_list = list(node.attrib)
        return len(attrib_list) != 0 

    # Gets the value of 
    def Value(self, tag : str, db_mode : str = "current") -> str:
        if (db_mode != "current"):
            self.current_mode = db_mode

        toBeReturned = ""
        toBeReturned = self.FindNode_impl(tag)

        return toBeReturned

    # Given the value, get the name of the attribute assigned to it
    def ValueName(self, tag : str, db_mode : str = "current") -> str:
        if (db_mode != "current"):
            self.current_mode = db_mode

        toBeReturned = ""
        toBeReturned = self.FindNodeReverse_impl(tag)
        
        return toBeReturned

    # implementation of find node, should not be called directly
    # but is called by utility functions provided by this class
    # impl implies not exposed to the user
    def FindNode_impl(self, tag : str) -> str:   
        root = self.Root()
        
        _list = []
        self.find_nodes_with_attrib(root, tag, _list)

        returnedList = []
        for item in _list:
            if (self.has_children(item)):
                childList = []
                self.find_children_rec(item, childList)
                for child in childList:
                    for attrib in child.attrib:
                        strAttrib = str(child.get(attrib))
                        returnedList.append(strAttrib)
            else:
                for attrib in item.attrib:
                    strAttrib = str(item.get(attrib))
                    if attrib == tag:
                        returnedList.append(strAttrib)

        # return the first for now, only temporary
        if len(returnedList) > 0:
            return returnedList[0]

        # not found
        return ""

    # impl implies not exposed to the user
    def FindNodeReverse_impl(self, tag : str) -> str:
        root = self.Root()
      
        # search the entire database - we can't narrow the search here
        _list = [] 
        self.find_children_rec(root, _list)
       
        returnedList = []
        for item in _list:
            if (self.has_children(item)):
                childList = []
                self.find_children_rec(item, childList)
                for child in childList:
                    for attrib in child.attrib:
                        # get values
                        if child.get(attrib) == tag or child.tag == tag:
                            returnedList.append(attrib)
            else:
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
    def Values(self, tag : str, db_mode : str) -> list:
        self.current_mode = db_mode
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

    def AllNodeNames(self, db_mode : str) -> list:
        self.current_mode = db_mode
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
    def LevelList(self, level_list_structure_out : LevelList, int_level : int = 0, node : str = None) -> None:
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
    def AttributesForNodeName(self, str_node_name : str, db_mode : str) -> list:
        self.current_mode = db_mode
        values = Values(str_node_name)
        for value in values:
            logger.Log(str(value.tag))
        return Values(str_node_name)