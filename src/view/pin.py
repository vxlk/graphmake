# represents the gui view of a pin ... 
# maybe just throw this on node
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#ignores the controller for now ... refactor later
from model.pin_model import *

class PinWidget(QWidget):
    def __init__(self, x, y, isInput = False, width = 10, height = 10):
        super().__init__()
        self.m_x = x
        self.m_y = y
        self.m_width = width
        self.m_height = height
        self.isSelected = False
        #not going thru controller, dunno if big poop or not
        self.backendPin = Pin(isInput)

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

def create_input_pin_widget(x, y):
    return PinWidget(x, y, True)
def create_output_pin_widget(x, y):
    return PinWidget(x, y, False)