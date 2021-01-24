from util.xml import *
from model.db.db_module.converter import *

# keeps track of transactions
class Database():
    def __init__(self):
        self.parser = XMLUtil()
        self.converter = XMLConverter()
        self.parser.SetMode(self.parser.funcMode)

    #todo: eventually implement transactions ... too lazy to do it right now

    # Convert from name_string to Node by reaching into the database and converting
    def Node(self, name_string):
        string = self.converter.ConvertToNode(self.parser.Value(name_string))
        if string is None:
            return "None"
        return string

    # Get the highest root parent of this node to classify it as a type
    def NodeParent(self, name_string):
        # we will be using "parent below root" nodes to classify variables by type
        self.parser.ParentBelowRootSuckWay(name_string)
        return self.parser.string_result

    # Get all node names in the current document
    def AllNodeNames(self):
        return self.parser.AllNodeNames()

    # Get all attributes out of a node
    def AttributesForNodeName(self, str_node_name):
        return self.parser.AllAttributes(str_node_name)

    # Return which document we are currently reading/writing (function/variable db)
    def CurrentMode(self):
        return self.parser.Mode()

# global instance
database = Database()