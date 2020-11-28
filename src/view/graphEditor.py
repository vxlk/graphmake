from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.node import NodeWidget

class GraphEditor(QAbstractScrollArea):
    
    updateSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._nodes = []
        # make a signal that broadcasts the node changes
    
    def genCmakeText(self):
        text = "" #reset the text before filling it in
        for node in self._nodes:
            text += node.text() + "\n"
        return text

    # event hooks    
    def mousePressEvent(self, e):
        wasInsideANode = False
        for node in self._nodes:
            if node.asRect().contains(e.pos()):
                #set as the one to be moved ...
                node.isSelected = True
                wasInsideANode = True
        if wasInsideANode == False:        
            self._nodes.append(NodeWidget(e.pos().x(), 
                                          e.pos().y()))
        super().mousePressEvent(e)
        self.viewport().update()
    
    def mouseReleaseEvent(self, e):
        for node in self._nodes:
            node.isSelected = False
        super().mouseMoveEvent(e)
        self.viewport().update()

    def mouseMoveEvent(self, e):
        for node in self._nodes:
            if node.isSelected:
                #for now i am just going to translate,
                #eventually will want to offset position
                #based on movement from last frame
                node.setPos(e.pos().x(), e.pos().y())
        super().mouseMoveEvent(e)
        self.viewport().update()
    
    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self.viewport())
        for node in self._nodes:
            # draw rect with text in the middle
            painter.fillRect(node.asRectF(), node.brush())
            painter.drawRect(node.asRect())
            painter.drawText(node.posText().x(), 
                             node.posText().y(), 
                             node.name())
            # draw pins --- SERIOUSLY NEEDS REWORKED ---
            i = 0
            for pin in node.pins:
                w = 16
                h = 16
                painter.fillRect(node.pinPos(pin.isInput, i).x() 
                                 if pin.isInput 
                                 else node.pinPos(pin.isInput, i).x() + node.m_width,
                                 node.pinPos(pin.isInput, i).y(), w * 0.2, w * 0.5, 
                                 node.brush()
                                 )
                i+=1
        codeString = self.genCmakeText()
        self.updateSignal.emit(codeString)