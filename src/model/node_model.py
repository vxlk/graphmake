from PyQt5.QtCore import *
import uuid
from model.db.db_module.db_model import *
from util.level_list import *

# Manager of nodes:
# Has knowledge of all nodes that exist
# Manages how other objects access certain nodes
# Manages how other objects query the database for the nodes
class NodeManager():
    def __init__(self):
        self.node_names = []
        self.attrib_name_dict = {}
        self.BuildNameDict()
        self.bad_node_guid = uuid.uuid4()

        self.selected_type_function = "Function"
        self.selected_type_variable = "Variable"

        self.current_node_name = "cmake_version" # this can be changed later
        self.current_node_type = self.selected_type_function

    # 1. Fills the list of all node names
    # 2. Fills the dictionary of names and associated code snippets with those names
    # Used on construction of the node manager
    def BuildNameDict(self):
        name_array = database.AllNodeNames()
        logger.Log(name_array)
        self.node_names = name_array
        for node_name in self.node_names:
            self.attrib_name_dict[node_name] = database.parser.Values(node_name)

    # Build a "level list" from the functions database
    # Level List is a dictionary that categorizes a type based on the level in the xml hierarchy
    # 0 - root, 1 - next, 2 - etc each level will have n number of keys associated
    def BuildLevelListFunctions(self):
        database.parser.SetMode(database.parser.funcMode)
        level_list = LevelList()
        database.parser.LevelList(level_list)
        return level_list

    # Build a "level list" from the variable database
    # Level List is a dictionary that categorizes a type based on the level in the xml hierarchy
    # 0 - root, 1 - next, 2 - etc each level will have n number of keys associated
    def BuildLevelListVariables(self):
        database.parser.SetMode(database.parser.varMode)
        level_list = LevelList()
        database.parser.LevelList(level_list)
        return level_list

nodeManager = NodeManager()

# Represents a node from the backend, a node will be shown on the front end by a rectangle
# for now i am electing to represent both variables
# and functions under the single node class: subject
# to change
class Node(QObject):
    def __init__(self):
        super().__init__()

        # set db path to the right direction
        if nodeManager.current_node_type == nodeManager.selected_type_function:
            database.parser.SetMode(database.parser.funcMode)
        else:
            database.parser.SetMode(database.parser.varMode)
    
        # variables
        self.name = nodeManager.current_node_name
        self.code = database.Node(self.name)
        self.guid = None
        self.input_pins = []
        self.is_function_node = True
        self.parent_name = database.NodeParent(self.name) # the current *type* identifier
        self.args = {} # if the node is a function, what variables are part of the code
        self.private_fill_in_arg_list()

    def SetNodeName(self, str_name):
        self.name = str_name

    def AddInput(self, other_node):
        self.input_pins.append(other_node)

    def RemoveInput(self, other_node):
        self.input_pins.append(other_node)

    # If this variable argument exists in the code of this node -> return true
    def ContainsVar(self, parent_name):
        for key in self.args.keys():
            if key == parent_name:
                return True
        return False

    # insert a variable into the slot given the name of the variable node
    # for now, does not take into account position of the argument in the function
    def InsertVariable(self, variable_node):
        assert variable_node.is_function_node == False
        #todo: decide positioning if multiple variables of the same name exist in the code block
        self.code = self.code.replace('%' + variable_node.parent_name + '%', variable_node.code, 1)

    # for internal use on construction, create a list of variables associated with this function node
    def private_fill_in_arg_list(self):
        # fill in the arg list with defaults
        for arg_key in database.converter.GetVars(self.code):
            self.args[arg_key] = ""


