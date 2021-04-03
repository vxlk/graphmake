from util.xml import *
from model.db.db_module.converter import *

# keeps track of transactions
class Database():
    def __init__(self):
        self.parser = XMLUtil()
        self.converter = XMLConverter()
        self.parser.current_mode = DBMode.functionMode

    #todo: eventually implement transactions ... too lazy to do it right now

    # Convert from name_string to Node by reaching into the database and converting
    def Node(self, name : str) -> str:
        string = self.converter.ConvertToNode(self.parser.Value(name))
        if string is None:
            return "None"
        return string

    # Get the highest root parent of this node to classify it as a type
    def NodeParent(self, name : str) -> str:
        # we will be using "parent below root" nodes to classify variables by type
        highest_level_parent = self.parser.ParentBelowRoot(name)
        return highest_level_parent

    # Get all node names in the current document
    def AllNodeNames(self) -> list:
        return self.parser.AllNodeNames(self.parser.current_mode)

    # Get all attributes out of a node
    def AttributesForNodeName(self, node_name : str) -> list:
        return self.parser.AllAttributes(node_name)

    # Return which document we are currently reading/writing (function/variable db)
    def CurrentMode(self) -> str:
        return self.parser.current_mode

# global instance
database = Database()