from PyQt5.QtGui import *
from PyQt5.QtCore import *
#ignores the controller for now ... refactor later
from model.node_model import Node

# represents a node in gui view, can communicate with the model through the controller by name (for now name == guid)
# for now make a node hold a QRect, QRectF, and QBrush (for color)
class NodeWidget:
    def __init__(self, x, y, width = 100, height = 100):
        self.m_x = x
        self.m_y = y
        self.m_width = width
        self.m_height = height
        self.isSelected = False
        self.backendNode = Node()

        #default color
        self.m_color = Qt.BrushStyle(Qt.blue)
        self.m_brush = QBrush(Qt.blue)

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
        return QPos(self.m_x, self.m_y)

    def asRect(self):
        return QRect(self.m_x, self.m_y, 
                     self.m_width, self.m_height)
    
    def asRectF(self):
        return QRectF(self.asRect())

    def brush(self):
        return self.m_brush
    
    def color(self):
        return self.m_color