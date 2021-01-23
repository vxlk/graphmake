from util.xml import *
from model.db.db_module.converter import *

# keeps track of transactions
class Database():
    def __init__(self):
        self.parser = XMLUtil()
        self.converter = XMLConverter()
        self.parser.SetMode(self.parser.funcMode)

        #todo: eventually implement transactions ... too lazy to do it right now

    def Node(self, name_string):
        string = self.converter.ConvertToNode(self.parser.Value(name_string))
        if string is None:
            return "None"
        return string

    def NodeParent(self, name_string):
        # we will be using "parent below root" nodes to classify variables by type
        result_str = ""
        self.parser.ParentBelowRootSuckWay(name_string, result_str)
        return result_str

    def AllNodeNames(self):
        return self.parser.AllNodeNames()

    def AttributesForNodeName(self, str_node_name):
        return self.parser.AllAttributes(str_node_name)

# global instance
database = Database()