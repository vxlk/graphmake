# represents a connection between two pins in the gui
# gonna need a backend that contains the two pins
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ConnectionWidget(QWidget):
    def __init__(self, pinWidgetInput, pinWidgetOutput):
        super().__init__()
        # going to have problems here where these references
        # will become stale, don't know python enough
        # to have a solution for this
        self.m_input = pinWidgetInput
        self.m_output = pinWidgetOutput
        self.isSelected = False
        #default color
        self.m_color = Qt.black
        self.m_brush = QBrush(self.m_color)

    # setters
    def setColor(self, color):
        self.m_color = color
        self.m_brush = QBrush(self.color)
    # no pos setters yet, idk how to handle it

    # getters
    def brush(self):
        return self.m_brush
    def color(self):
        return self.m_color
    def inputPos(self):
        return self.m_input.pos()
    def outputPos(self):
        return self.m_output.pos()