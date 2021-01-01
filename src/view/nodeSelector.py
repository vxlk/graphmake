from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.node import *

# for now i shall make a list of the names, eventually i want pictures
# like draw.io has

class NodeSelectorWidget(QDockWidget):

    def __init__(self):
        super().__init__()

    def CurrentNodeName(self):
        return nodeManager.current_node_name
