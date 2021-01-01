from PyQt5.QtCore import *
import uuid
from model.db.db_module.db_model import *

class NodeManager():
    def __init__(self):
        self.node_names = []
        self.attrib_name_dict = self.BuildNameDict()
        self.current_node_name = "cmake_version" # this can be changed later

    def BuildNameDict(self):
        logger.Log("BuildNameDict")
        name_array = database.AllNodeNames()
        logger.Log(name_array)
        node_names = name_array
        for node_name in self.node_names:
            attrib_name_dict[node_name] = Values(node_name)

nodeManager = NodeManager()

# Represents a node from the backend, a node will be shown on the front end by a rectangle
class Node(QObject):
    def __init__(self):
        super().__init__()
        self.name = nodeManager.current_node_name
        self.code = database.Node(self.name)
        self.guid = uuid.uuid4()

    def SetNodeName(self, str_name):
        self.name = str_name


