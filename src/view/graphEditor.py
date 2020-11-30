from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.node import NodeWidget

class GraphEditor(QAbstractScrollArea):
    
    updateSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._nodes = []
        self.drawConnection = False
        self.connectionStartPoint = QPoint(0,0)
        self.connectionEndPoint = QPoint(0,0)
        self.setMouseTracking(True)
        # enable this later if needed if we need a
        # custom event loop
        #self.installEventFilter(self)
    
    def genCmakeText(self):
        text = "" #reset the text before filling it in
        for node in self._nodes:
            text += node.text() + "\n"
        return text

    # event hooks    
    def mousePressEvent(self, e):
        # reset our draw event loop
        if self.drawConnection:
            self.drawConnection = False
            return

        wasInsideANodeOrPin = False
        for node in self._nodes:
            if node.asRect().contains(e.pos()):
                #set as the one to be moved ...
                node.isSelected = True
                wasInsideANodeOrPin = True
            else:
                for pin in node.pins:
                    if pin.asCircle().contains(e.pos()):
                        pin.isSelected = True
                        wasInsideANodeOrPin = True
                        self.drawConnection = True
                        self.connectionStartPoint = e.pos()
                        self.connectionEndPoint = e.pos()

        if wasInsideANodeOrPin == False:        
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
        if self.drawConnection:
            self.connectionEndPoint = e.pos()
        
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

        # draw line
        if self.drawConnection:
            painter.setBrush(Qt.black)
            painter.drawLine(self.connectionStartPoint, self.connectionEndPoint)
        
        # render nodes and pins
        for node in self._nodes:
            painter.setBrush(node.color())
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
                
                if self.drawConnection:
                    if pin.asCircle().contains(self.connectionEndPoint):
                        pin.setSize(20,20)
                    else:
                        pin.setSize(10,10)

                pinPointX = pin.pos().x()
                pinPointY = pin.pos().y()
                pinWidth = pin.m_width
                pinHeight = pin.m_height

                painter.setBrush(pin.color())

                # maybe do later but just the circles looks good for now
                #painter.fillRect(pinPointX,
                #                 pinPointY, 
                #                 w * 0.2, w * 0.5, 
                #                 node.brush()
                #                 )
                if pin.isInput():
                    painter.drawEllipse(pinPointX - 10, pinPointY, pinWidth, pinHeight)
                else:
                    painter.drawEllipse(pinPointX, pinPointY, pinWidth, pinHeight)
                i+=1
        codeString = self.genCmakeText()
        self.updateSignal.emit(codeString)