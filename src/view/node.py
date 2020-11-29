from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#ignores the controller for now ... refactor later
from model.node_model import Node
from model.pin_model import *

# represents a node in gui view, can communicate with the model through the controller by name (for now name == guid)
# for now make a node hold a QRect, QRectF, and QBrush (for color)
class NodeWidget(QWidget):
    def __init__(self, x, y, width = 100, height = 100):
        super().__init__()
        self.m_x = x
        self.m_y = y
        self.m_width = width
        self.m_height = height
        self.isSelected = False
        #not going thru controller, dunno if big poop or not
        self.backendNode = Node()

        self.pins = []
        # add an output
        self.pins.append(create_output_pin())
        # add an input
        self.pins.append(create_input_pin())
        
        #default color
        self.m_color = Qt.BrushStyle(Qt.blue)
        self.m_brush = QBrush(Qt.blue)
        self.m_brush.setStyle(Qt.SolidPattern)

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

    def posText(self):
        return QPoint(self.pos().x() + self.m_width/2,
                      self.pos().y() + self.m_height/2)

    def asRect(self):
        return QRect(self.m_x, self.m_y, 
                     self.m_width, self.m_height)
    
    def asRectF(self):
        return QRectF(self.asRect())

    def brush(self):
        return self.m_brush
    
    def color(self):
        return self.m_color

    def name(self):
        return self.backendNode.name

    def text(self):
        return self.backendNode.code

    # should send num from 0 index
    def pinPos(self, isInput, num):
        denom = num + 2
        if denom > 4:
            denom = 2
            numerator = num
        else: 
            numerator = 1
        return QPoint(self.pos().x(),
                      self.pos().y() + numerator/denom) if isInput else QPoint(self.pos().x(),
                                                                        self.pos().y() - numerator/denom)

        