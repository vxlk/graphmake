from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from model.node_model import *
from view.pin import *

# represents a node in gui view, can communicate with the model by name (for now name == guid)
# for now make a node hold a QRect, QRectF, and QBrush (for color)
class NodeWidget(QWidget):
    def __init__(self, x, y, width = 100, height = 100):
        super().__init__()
        self.m_x = x
        self.m_y = y
        self.m_width = width
        self.m_height = height
        self.isSelected = False
        self.backendNode = Node()

        self.pins = []
        # add an output
        outputPos = self.pinPos(False, 0)
        self.pins.append(create_output_pin_widget(outputPos.x(), outputPos.y(), self.backendNode))
        # add an input
        inputPos = self.pinPos(True, 0)
        self.pins.append(create_input_pin_widget(inputPos.x(), inputPos.y(), self.backendNode))
        
        self.m_color = None
        #default color
        if nodeManager.current_node_type == nodeManager.selected_type_function:
            self.m_color = Qt.blue
        else:
            self.m_color = Qt.red

        self.m_brush = QBrush(self.m_color)
        self.m_brush.setStyle(Qt.SolidPattern)

    # setters
    def setSize(self, width, height):
        self.m_width = width
        self.m_height = height
    
    def setColor(self, color):
        self.m_color = color
        self.m_brush.setColor(color)

    def setPos(self, x, y):
        self.m_x = x
        self.m_y = y
        i = 0
        for pin in self.pins:
            pinPos = self.pinPos(pin.isInput(), i)
            pin.setPos(pinPos.x(), pinPos.y())
            i+=1

    # getters
    def pos(self):
        return QPoint(self.m_x, self.m_y)

    def posText(self):
        return QPoint(self.pos().x() + self.m_width/4,
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

    # this function used to be used to connect a node's code with any connected nodes code
    # this is now handled on connection and the full code with the inputted args is all
    # returned by the code variable.  Keeping this function as a wrapper around this 
    # variable in case extra functionality is needed in the future
    def text(self):
        toBeReturned = self.backendNode.code
        return toBeReturned

    def inputPins(self):
        inputList = []
        for pin in self.pins:
            if pin.isInput():
                inputList.append(pin)
        return inputList

    def outputPins(self):
        outputList = []
        for pin in self.pins:
            if pin.isInput() == False:
                outputList.append(pin)
        return outputList

    def posContainsPin(self, pos):
        for pin in self.pins:
            if pin.asCircle().contains(pos):
                return True
        return False

    # should send num from 0 index
    def pinPos(self, isInput, num, size=10):
        denom = num + 2
        if denom > 4:
            denom = 2
            numerator = num
        else: 
            numerator = 1
        return QPoint(self.pos().x() - size,
                      self.pos().y() + numerator/denom) if isInput else QPoint(self.pos().x() + self.m_width,
                                                                        self.pos().y() - numerator/denom)

    def AddConnection(self, other_node):
        self.backendNode.AddInput(other_node)

    def RemoveConnection(self, other_node):
        self.backendNode.RemoveInput(other_node)

    def SetSelected(self, bool_is_selected):
        self.isSelected = bool_is_selected
        if bool_is_selected:
            # we do it this way to save the old color
            self.m_brush.setColor(Qt.green)
        else:
            self.setColor(self.m_color)
        