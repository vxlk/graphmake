from PyQt5.QtWidgets import *

class TooltipContentDecorator(object):
    def __init__(self):
        self.text = ""
        self.color = None
        self.font = None
        self.img = None

class TooltipHyperlink(TooltipContentDecorator):
    def __init__(self, text, color = None, font = None):
        super().__init__()

# https://stackoverflow.com/questions/24392059/display-a-qdialog-on-mouse-over
class Tooltip(object):
    """description of class"""
    def __init__(self, parent : QWidget, txt : str, x : int, y : int, link : str = None):
        self.decorators = []
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100

        self.handle = QDialog(parent)
        tooltip_label = QLabel(self.handle)
        tooltip_label.setText("message")
        self.handle.setFixedSize(self.height, self.width)
        self.handle.move(x,y)
        self.handle.show()

    #def make_doc_tooltip(self, txt : str, x : int, y : int, link : str = None) -> QDialog: # dunno if this should return it and someone else manages it?
        
       # return dialog


