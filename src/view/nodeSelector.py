from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.node_model import *
from util.xml import *
from util.level_list import *

# for now i shall make a list of the names, eventually i want pictures
# like draw.io has
# This tree works directly with the node manager to figure out which nodes/vars to draw
class NodeSelectorTree():
    def __init__(self):
        super().__init__()
        self.tree_impl = QTreeWidget()
        self.tree_impl.resize(250, self.tree_impl.height()) #todo: figure out size
        # might need to reorganize this later... for now just do an array
        self.items_func = []
        self.items_var = []
        self.tree_impl.setColumnCount(2)
        
        self.selected_type = nodeManager.selected_type_function

        # --- Functions ----
        level_list = nodeManager.BuildLevelListFunctions()
        # loop thru level list
        level = level_list.FirstLevel()
        while level != None:
            node = level.First()
            while node != None:
                # create a tree item with parent from the node parent
                item = QTreeWidgetItem(self.FindTreeItemFunction(node.Up()))
                item.setText(0, node.Data()) # hardcoded 0 .. enforce 1 name?
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                self.items_func.append(item)

                node = level.Next()

            level = level.Next()

        # --- Variables ----
        level_list = nodeManager.BuildLevelListVariables()        
        # loop thru level list
        level = level_list.FirstLevel()
        while level != None:
            node = level.First()
            while node != None:
                # create a tree item with parent from the node parent
                item = QTreeWidgetItem(self.FindTreeItemVariable(node.Up()))
                item.setText(1, node.Data()) # hardcoded 0 .. enforce 1 name?
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                self.items_var.append(item)

                node = level.Next()

            level = level.Next()
                    


        #prev_node_level = 0
        #prev_dict = {}
        #prev_node_name = ""
        #level_list = nodeManager.BuildLevelListFunctions()
        #for item_name in level_list.keys():
        #    current_level = level_list[item_name]
        #    # ------- functions --------
        #     # create new parent
        #    if current_level > prev_node_level:
        #        prev_node_level = current_level
        #        prev_dict[current_level] = prev_node_name
        #    elif current_level < prev_node_level:
        #        prev_node_level = current_level
        #        prev_dict[current_level] = item_name

        #    if current_level in prev_dict:
        #        item = QTreeWidgetItem(self.FindTreeItemFunction(prev_dict[current_level]))
        #    # root
        #    else:
        #        item = QTreeWidgetItem(self.FindTreeItemFunction(""))
        #    item.setText(0, item_name) # hardcoded 0 .. enforce 1 name?
        #    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)

        #    prev_node_name = item_name
        #    self.items_func.append(item)

        #    # -------- variables ---------
        #prev_node_level = 0
        #prev_dict = {}
        #prev_node_name = ""
        #level_list = nodeManager.BuildLevelListVariables()
        #for item_name in level_list.keys():
        #    current_level = level_list[item_name]

        #     # create new parent
        #    if current_level > prev_node_level:
        #        prev_node_level = current_level
        #        prev_dict[current_level] = prev_node_name
        #    elif current_level < prev_node_level:
        #        prev_node_level = current_level
        #        prev_dict[current_level] = item_name

        #    if current_level in prev_dict:
        #        item = QTreeWidgetItem(self.FindTreeItemVariable(prev_dict[current_level]))
        #    # root
        #    else:
        #        item = QTreeWidgetItem(self.FindTreeItemVariable(""))

        #    item.setText(1, item_name) # hardcoded 0 .. enforce 1 name?
        #    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)

        #    prev_node_name = item_name
        #    self.items_var.append(item)


        self.tree_impl.itemClicked.connect(self.onNodeItemClick)
        self.tree_impl.topLevelItem(0).setSelected(True)

    # the node we are currently highlighted on in the tree
    def CurrentNodeName(self):
        return nodeManager.current_node_name

    # Return a list of all node names available from the node manager
    def AllNodeNames(self):
        return nodeManager.node_names # might want the dict?

    # Get the underlying widget that this object wraps
    def Widget(self):
        return self.tree_impl

    # the slot that happens when something in the tree view is clicked,
    # until the tree is redesigned, it will do some arbitrary dumb checks
    # to decide whether it is a var or a function
    def onNodeItemClick(self, item, index):
        node_name = ""
        # is a var
        if (item.text(0) == ""):
            node_name = item.text(1)
            self.selected_type = nodeManager.selected_type_variable
        else:
            node_name = item.text(0)
            self.selected_type = nodeManager.selected_type_function

        nodeManager.current_node_type = self.selected_type
        nodeManager.current_node_name = node_name # hardcoded 0 .. enforce 1 name?

    # Search the list of function nodes in the tree for the qtreeitem
    def FindTreeItemFunction(self, str_node_name):
        if str_node_name == None:
            return self.tree_impl
        for item in self.items_func:
            #print(item.text(0) + "," + str_node_name)
            if item.text(0) == str_node_name:
                #print("found")
                return item
        #print("not found")
        return self.tree_impl

    # Search the list of variable nodes in the tree for the qtreeitem
    def FindTreeItemVariable(self, str_node_name):
        if str_node_name == None:
            return self.tree_impl
        for item in self.items_var:
            #print(item.text(0) + "," + str_node_name)
            if item.text(1) == str_node_name:
                #print("found")
                return item
        #print("not found")
        return self.tree_impl