from PyQt5.QtCore import *
import uuid
from model.db.db_module.db_model import *

class NodeManager():
    def __init__(self):
        self.node_names = []
        self.attrib_name_dict = {}
        self.BuildNameDict()

        self.selected_type_function = "Function"
        self.selected_type_variable = "Variable"

        self.current_node_name = "cmake_version" # this can be changed later
        self.current_node_type = self.selected_type_function

    def BuildNameDict(self):
        name_array = database.AllNodeNames()
        logger.Log(name_array)
        self.node_names = name_array
        for node_name in self.node_names:
            self.attrib_name_dict[node_name] = database.parser.Values(node_name)

    def BuildLevelListFunctions(self):
        database.parser.SetMode(database.parser.funcMode)
        level_list = {}
        database.parser.LevelList(level_list)
        return level_list

    def BuildLevelListVariables(self):
        database.parser.SetMode(database.parser.varMode)
        level_list = {}
        database.parser.LevelList(level_list)
        print(level_list)
        return level_list

nodeManager = NodeManager()

# Represents a node from the backend, a node will be shown on the front end by a rectangle
# for now i am electing to represent both variables
# and functions under the single node class: subject
# to change
class Node(QObject):
    def __init__(self):
        super().__init__()
        self.name = nodeManager.current_node_name
        self.code = database.Node(self.name)
        self.guid = uuid.uuid4()

    def SetNodeName(self, str_name):
        self.name = str_name


