from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.node_model import *

from util.xml import *

# for now i shall make a list of the names, eventually i want pictures
# like draw.io has

class NodeSelectorTree():
    def __init__(self):
        super().__init__()
        self.tree_impl = QTreeWidget()
        self.tree_impl.resize(128, self.tree_impl.height()) #todo: figure out size
        # might need to reorganize this later... for now just do an array
        self.items = []
        self.tree_impl.setColumnCount(1)

        prev_node_level = 0
        prev_dict = {}
        prev_node_name = ""
        level_list = nodeManager.BuildLevelList()
        for item_name in level_list.keys():
            current_level = level_list[item_name]

             # create new parent
            if current_level > prev_node_level:
                prev_node_level = current_level
                prev_dict[current_level] = prev_node_name
            elif current_level < prev_node_level:
                prev_node_level = current_level
                prev_dict[current_level] = item_name

            if current_level in prev_dict:
                item = QTreeWidgetItem(self.FindTreeItem(prev_dict[current_level]))
            # root
            else:
                item = QTreeWidgetItem(self.FindTreeItem(""))
            item.setText(0, item_name) # hardcoded 0 .. enforce 1 name?
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)

            prev_node_name = item_name
            self.items.append(item)

        self.tree_impl.itemClicked.connect(self.onNodeItemClick)
        self.tree_impl.topLevelItem(0).setSelected(True)

        for item in self.items:
            print(item.parent())
        #nodeManager.BuildLevelList()

    def CurrentNodeName(self):
        return nodeManager.current_node_name

    def AllNodeNames(self):
        return nodeManager.node_names # might want the dict?

    def Widget(self):
        return self.tree_impl

    def onNodeItemClick(self, item, index):
        nodeManager.current_node_name = item.text(0) # hardcoded 0 .. enforce 1 name?

    def FindTreeItem(self, str_node_name):
        for item in self.items:
            #print(item.text(0) + "," + str_node_name)
            if item.text(0) == str_node_name:
                #print("found")
                return item
        #print("not found")
        return self.tree_impl