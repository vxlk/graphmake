# represents the gui view of a pin ... 
# maybe just throw this on node
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from model.pin_model import *
from view.connection import ConnectionWidget
from util.utilities import __deprecated__

# The gui view of a pin as well as the model of the pin
# pin's backend data is held within the gui
# pins are only used to make the gui representation more straight forward
# and are essentially just mediators between adding variables to node code
class PinWidget(QWidget):
    def __init__(self, x, y, node_owner, isInput = False, width = 10, height = 10):
        super().__init__()
        self.m_x = x
        self.m_y = y
        self.m_width = width
        self.m_height = height
        self.isSelected = False
        self.backendPin = Pin(isInput)
        self.connections = []

        self.node_owner = node_owner
        self.connected_nodes = []

        #default color
        self.m_color = Qt.black

        if self.isInput():
            self.m_color = Qt.green
        else:
            self.m_color = Qt.red

        self.m_brush = QBrush(self.m_color)

     # setters
    def setSize(self, width, height):
        self.m_width = width
        self.m_height = height
    
    def setColor(self, color):
        self.m_color = color
        self.m_brush = QBrush(self.color)

    def setPos(self, x, y):
        self.m_x = x
        self.m_y = y

    # getters
    def pos(self):
        return QPoint(self.m_x, self.m_y)
    def brush(self):
        return self.m_brush
    def isInput(self):
        return self.backendPin.isInput
    def color(self):
        return self.m_color
    def asCircle(self):
        return QGraphicsEllipseItem(self.m_x, self.m_y, 
                                    self.m_width, self.m_height)

    # add a connection to this pin on this node if the variable classification
    # fits one of the slots that the node's code has open.  Does not take into
    # account position right now
    def TryAddConnection(self, otherPin):
        inputPin = self if self.isInput else otherPin
        outputPin = self if self.isInput == False else otherPin
        if inputPin.node_owner.ContainsVar(outputPin.node_owner.parent_name):
            self.connections.append(ConnectionWidget(inputPin, outputPin))
            outputPin.connected_nodes.append(outputPin.node_owner)
            # here we need to handle replacing the var with the actual code of the var
            # this logic used to be contained within converter, decide if it should be
            # kept there, moved to node, etc
            inputPin.node_owner.InsertVariable(outputPin.node_owner)
            return True
        return False

    # as of 1/24/2021 pins no longer hold their own code -> consider removal
    def text(self):
        __deprecated__("Pins no longer hold their own code")
        text = ""
        #for output in self.outputConnections:
         #   text += output.backendPin.outputCode
        return text

# Wrappers around creating pins (syntactic sugar around creation)
def create_input_pin_widget(x, y, node_owner):
    return PinWidget(x, y, node_owner, True)
def create_output_pin_widget(x, y, node_owner):
    return PinWidget(x, y, node_owner, False)