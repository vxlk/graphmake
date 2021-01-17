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

    def AllNodeNames(self):
        return self.parser.AllNodeNames()

    def AttributesForNodeName(self, str_node_name):
        return self.parser.AllAttributes(str_node_name)

# global instance
database = Database()