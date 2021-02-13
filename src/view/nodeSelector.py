from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.node_model import *
from model.db.db_module import *
from util.xml import *
from util.level_list import *

# for now i shall make a list of the names, eventually i want pictures
# like draw.io has
# This tree works directly with the node manager to figure out which nodes/vars to draw
class NodeSelectorTree(QObject):

    # emit that a function tree item was clicked, and filter based on this
    filterSignal = pyqtSignal(object)

    def __init__(self, type_of_tree):
        super().__init__()
        self.tree_impl = QTreeWidget()
        self.tree_impl.resize(250, self.tree_impl.height()) #todo: figure out size
        # might need to reorganize this later... for now just do an array
        self.items_func = []
        self.items_var = []
        self.tree_impl.setColumnCount(1)
        self.type_of_tree = type_of_tree # is set to var / function when the tree is created
        self.selected_type = "" # changes depending on click
        if type_of_tree == "Function":
            self.selected_type = nodeManager.selected_type_function
        if type_of_tree == "Variable":
            self.selected_type = nodeManager.selected_type_variable

        if (type_of_tree == "Function"):
            # --- Functions ----
            level_list = nodeManager.BuildLevelListFunctions()
            #level_list.Print()
            # loop thru level list
            level = level_list.FirstLevel()
            node = level.First()
            while node != None:
                # create a tree item with parent from the node parent
                self.AddToTree(node, True)

                # recurse through children until there are no more children
                child = node.Down()
                while child != None:
                    # create a tree item with parent from the node parent
                    self.AddToTree(child, True)
                    childs_parent = child.Up()

                    ## look left for a neighbor on the row that we are looking @, until we can't anymore
                    neighbor = child.Left()
                    while neighbor != None and neighbor.Up() == childs_parent:
                        # create a tree item with parent from the node parent
                        self.AddToTree(neighbor, True)
                        # get the next node in this row
                        neighbor = neighbor.Left()

                    # get the next child down
                    child = child.Down()
                    
                # go through nodes on a level
                node = level.Next()

        if (type_of_tree == "Variable"):
            ## --- Variables ----
            level_list = nodeManager.BuildLevelListVariables()
            #level_list.Print()
            # loop thru level list
            level = level_list.FirstLevel()
            node = level.First()
            while node != None:
                # create a tree item with parent from the node parent
                self.AddToTree(node, False)
                # recurse through children until there are no more children
                child = node.Down()
            
                while child != None:
                    # create a tree item with parent from the node parent
                    self.AddToTree(child, False)
                    childs_parent = child.Up()

                    ## look left for a neighbor on the row that we are looking @, until we can't anymore
                    neighbor = child.Left()
                    while neighbor != None and neighbor.Up() == childs_parent:
                        # create a tree item with parent from the node parent
                        self.AddToTree(neighbor, False)
                        # get the next node in this row
                        neighbor = neighbor.Left()

                    # get the next child down
                    child = child.Down()
                    
                # go through nodes on a level
                node = level.Next()
                    
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
        node_name = item.text(0)
        nodeManager.current_node_type = self.selected_type
        nodeManager.current_node_name = node_name # hardcoded 0
        if self.selected_type == nodeManager.selected_type_function:
            self.filterSignal.emit(nodeManager.current_node_name)

    # filter the variable view so that only variables that can be connected show up
    # as an option
    # added to greatly improve intuitive usability, at the cost of a bit of restriction
    @pyqtSlot(object)
    def onFilterEvent(self, str_node_name):
        if self.type_of_tree == "Variable":
            node = Node() # create a node using current settings
            for child in self.items_var:
                child.setHidden(True)
            for arg in node.args:
                for item in self.items_var:
                    if item.text(0) == arg:
                        item.setHidden(False)

    # Search the list of function nodes in the tree for the qtreeitem
    # wanna get the last item with this name so this is a little funky
    def FindTreeItemFunction(self, str_node_name):
        found_node = None
        if str_node_name == None:
            return self.tree_impl

        for item in self.items_func:
            if item.text(0) == str_node_name:
                found_node = item

        if found_node == None:
            return self.tree_impl
        else:
            return found_node

    # Search the list of variable nodes in the tree for the qtreeitem
    # wanna get the last item with this name so this is a little funky
    def FindTreeItemVariable(self, str_node_name):
        found_node = None
        if str_node_name == None:
            return self.tree_impl

        for item in self.items_var:
            if item.text(0) == str_node_name:
                found_node = item
  
        if found_node == None:
            return self.tree_impl
        else:
            return found_node

    # add an item to the tree
    # pick a section that it will belong to (the function section (left), or the variable section (right))
    def AddToTree(self, node, bool_is_func_node):
        # create a tree item with parent from the node parent
        node_parent_name = ""
        if node.Up() != None:
            node_parent_name = node.Up().Data()

        # add to tree with correct parent based on what type it is
        if bool_is_func_node == True:
            item = QTreeWidgetItem(self.FindTreeItemFunction(node_parent_name))
        else:
            item = QTreeWidgetItem(self.FindTreeItemVariable(node_parent_name))
  
        item.setText(0, node.Data())
        if item.text(0) != "Parent": # fucking hate this
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
    
        # add to internal list for easier searching based on what type it is
        if bool_is_func_node == True:
            self.items_func.append(item)
        else:
            self.items_var.append(item)