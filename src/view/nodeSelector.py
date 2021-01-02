from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.node_model import *

# for now i shall make a list of the names, eventually i want pictures
# like draw.io has

class NodeSelectorTree():
    def __init__(self):
        super().__init__()
        self.tree_impl = QTreeWidget()
        self.tree_impl.resize(128, self.tree_impl.height()) #todo: figure out size
        # might need to reorganize this later... for now just do an array
        self.items = []
        for item_name in self.AllNodeNames():
            item = QTreeWidget(tree_impl)
            item.setText(0, item_name)
            item.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
            self.items.append(item) 

    def CurrentNodeName(self):
        return nodeManager.current_node_name

    def AllNodeNames(self):
        return nodeManager.node_names # might want the dict?

    def Widget(self):
        return self.tree_impl



#class NodeSelectorWidget(QDockWidget):
 #   def __init__(self, string_name):
 #       super().__init__(string_name)
 #       tree_model = NodeSelectorTree()
 #       self.setWidget(tree_model.Widget())