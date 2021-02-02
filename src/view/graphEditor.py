from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.node import NodeWidget
from model.node_model import * # access the node manager
from model.graph import *

# HOOK UP TO BACKEND GRAPH!!!!!!!!!!!!!!!!!! ------------------------------------------------------------------

# Used when auto generating graphs
# Think of this as a matrix | node |      |
#                           |      | node |
# that provides a layout for incoming auto-generated graphs of nodes and variables
class GraphView():
    def __init__(self):
        none = None # todo: implement later im stressing out rn

class GraphEditor(QAbstractScrollArea):
    
    updateSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._nodes = []
        self.drawConnection = False
        self.connectionStartPoint = QPoint(0,0)
        self.connectionEndPoint = QPoint(0,0)
        self.setMouseTracking(True)
        self.current_graph = graphManager.TopLevelGraph()
        self.SetGraph(self.current_graph)

        # enable this later if needed if we need a
        # custom event loop
        #self.installEventFilter(self)
    
    def genCmakeText(self):
        text = "" #reset the text before filling it in
        for node in self._nodes:
            if node.backendNode.is_function_node:
                text += node.text()
                text += '\n'
        return text

    # set the current gui to mirror a new graph
    def SetGraph(self, incoming_graph):
        self.setObjectName(incoming_graph.name)
        self._nodes.clear()
        # todo: fill in this graph based on that graph

    def checkIfPinIsHit(self, pos):
        for node in self._nodes:
            if node.posContainsPin(pos):
                return True
        return False

    def getPinAtPos(self, pos):
        for node in self._nodes:
            for pin in node.pins:
                if pin.asCircle().contains(pos):
                    return pin
        return None

    # event hooks    
    def mousePressEvent(self, e):
        if self.checkIfPinIsHit(e.pos()):
            if self.drawConnection:
                # we have a connection
                pendingPin = self.getPinAtPos(e.pos())
                beginningPin = self.getPinAtPos(self.connectionStartPoint)
                if pendingPin is not None and beginningPin is not None:
                    if (pendingPin.isInput() and not beginningPin.isInput()
                    or not pendingPin.isInput() and beginningPin.isInput()):
                        inputPin = pendingPin if pendingPin.isInput() else  beginningPin
                        outputPin = pendingPin if not pendingPin.isInput() else beginningPin
                        # going to draw a double line for now
                        # todo: bad bad bad 
                        if pendingPin.TryAddConnection(beginningPin):
                            pendingPin.node_owner.AddInput(beginningPin)
                        else:
                            connection_error_dialog = QDialog()
                            connection_error_dialog.exec_()
                        #beginningPin.addConnection(pendingPin)

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
            newNodeWidget = NodeWidget(e.pos().x(), e.pos().y())
            newNodeWidget.backendNode.is_function_node = nodeManager.current_node_type == nodeManager.selected_type_function       
            self._nodes.append(newNodeWidget)
                
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
                
                painter.drawEllipse(pinPointX, pinPointY, pinWidth, pinHeight)
                i+=1

                for conn in pin.connections:
                    startPoint = conn.inputPos()
                    endPoint = conn.outputPos()
                    painter.setBrush(conn.color())
                    painter.drawLine(startPoint, endPoint)
        codeString = self.genCmakeText()
        self.updateSignal.emit(codeString)