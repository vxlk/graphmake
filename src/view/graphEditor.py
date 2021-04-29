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
# also holds the position of existing nodes in existing graphs
class GraphView():
    def __init__(self, str_name):
        self.node_widgets = [] # list of unordered nodes sent to the rendering pipeline
        self.var_widget_indices = {} # dictionary of connections used internally to keep track for rendering
        self.graph_name = str_name

        self.curr_pos_func = QPoint(25,25) # temp
        self.curr_pos_var = QPoint(200, 25)

    def CreateView(self, graph: Graph):
        # create func nodes
        for func in graph.nodes:
            func_node = func.name
            # tell us which backend node to use
            nodeManager.current_node_name = func_node
            nodeManager.current_node_type = nodeManager.selected_type_function

            if func.HasPosition():
                self.curr_pos_func = QPoint(func.x, func.y)            

            # make the node
            newNodeWidget = NodeWidget(self.curr_pos_func.x(), self.curr_pos_func.y())
            newNodeWidget.backendNode.guid = func.guid
            newNodeWidget.backendNode.is_function_node = True       
            self.node_widgets.append(newNodeWidget)
            self.TempIncreasePosFunc() # ++

        # create var nodes
        for var in graph.vars:
            var_node = var.name
            # tell us which backend node to use
            nodeManager.current_node_name = var_node
            nodeManager.current_node_type = nodeManager.selected_type_variable

            if var.HasPosition():
                self.curr_pos_var = QPoint(var.x, var.y)

            # make the node
            newNodeWidget = NodeWidget(self.curr_pos_var.x(), self.curr_pos_var.y())
            newNodeWidget.backendNode.guid = var.guid
            newNodeWidget.backendNode.is_function_node = False       
            self.node_widgets.append(newNodeWidget)
            self.TempIncreasePosVar() # ++

            # add this node to the var node index dictionary
            self.var_widget_indices[var_node] = 1

        # render connections
        for node_index in graph.connections.keys():
            list_connected_vars = graph.connections[node_index]
            for var_index in list_connected_vars:
                # Given a 1d array of nodes and names: keep track of the index of the node name we are currently on
                # use the next free one when applying a connection
                # n n n v1 v2 v1 v3
                # |     |
                # |        |
                #   |          |
                var = graph.vars[var_index]
                var_name = var.name
                current_index = 1
                current_var_index = self.var_widget_indices[var_name]
                # find the correct widget to connect to
                for widget in self.node_widgets:
                    if widget.backendNode.name == var_name:
                        if current_index == current_var_index:
                            # use this node: this should work bc we insert nodes then vars -> so graph.nodes == (subset of func nodes)node_widget
                            # also connect pins: for now just connect first pin
                            if (self.node_widgets[node_index].pins[0].TryAddConnection(widget.pins[0])):
                                self.node_widgets[node_index].backendNode.AddInput(widget.backendNode)
                            # mark this name as used
                            self.var_widget_indices[var_name] += 1
                        else:
                            current_index += 1
       
    def NodeWidgets(self):
        return self.node_widgets

    def TempIncreasePosFunc(self):
        curr_y = self.curr_pos_func.y()
        self.curr_pos_func.setY(curr_y + 105)

    def TempIncreasePosVar(self):
        curr_y = self.curr_pos_var.y()
        self.curr_pos_var.setY(curr_y + 105)
        

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
        self.graphViews = []
        self.graphViews.append(GraphView(self.current_graph.name))
        self.mouse_is_held_down = False

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
        # todo: check if graph view needs added
        self.setObjectName(incoming_graph.name)
        self._nodes.clear()
        curr_view = self.AddView(incoming_graph)
        self.current_view = curr_view
        self._nodes = curr_view.node_widgets
        # todo: fill in this graph based on that graph

    # add a view to the list if it is unique and update its view based on the current graph
    def AddView(self, graph: Graph):
        result = self.FindView(graph.name)
        # add if a new graph
        if result == None:
            self.graphViews.append(GraphView(graph))
            result = self.graphViews[len(self.graphViews)-1]
        # update the view
        result.CreateView(graph)
        return result
        
    # Find the view associated with this graph in order to render it
    def FindView(self, str_graph_name):
        for view in self.graphViews:
            if view.graph_name == str_graph_name:
                return view
        return None

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
        self.mouse_is_held_down = True
        self.ClearAllSelections()
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
                            self.current_graph.AddConnection(self.current_graph.NodeIndex(inputPin.node_owner.name), outputPin.node_owner.name)
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
                node.SetSelected(True)
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
            # if we don't have a valid selection - bail
            if nodeManager.current_node_type == nodeManager.selected_type_none:
                return
            newNodeWidget = NodeWidget(e.pos().x(), e.pos().y())
            newNodeWidget.backendNode.is_function_node = nodeManager.current_node_type == nodeManager.selected_type_function       
            #self._nodes.append(newNodeWidget)
            self.ClearAllSelections()
            newNodeWidget.SetSelected(True)

            # add func node to graph
            if newNodeWidget.backendNode.is_function_node:
                guid = self.current_graph.TryAddNode(newNodeWidget.backendNode.name, e.pos().x(), e.pos().y())
                # this one cant fail yet
                newNodeWidget.backendNode.guid = guid

            # add var node to graph
            else:
                guid = self.current_graph.TryAddVar(newNodeWidget.backendNode.name, None, e.pos().x(), e.pos().y())
                # this one can fail
                if guid != nodeManager.bad_node_guid:
                    newNodeWidget.backendNode.guid = guid
                
            self.current_view.node_widgets.append(newNodeWidget)

        super().mousePressEvent(e)
        self.viewport().update()
    
    def mouseReleaseEvent(self, e):
        self.mouse_is_held_down = False
        super().mouseMoveEvent(e)
        self.viewport().update()

    def mouseMoveEvent(self, e):
        if self.drawConnection:
            self.connectionEndPoint = e.pos()
        
        for node in self._nodes:
            if node.isSelected and self.mouse_is_held_down:
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
            painter.setBrush(node.brush())
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

    def keyPressEvent(self, e):
        super().keyPressEvent(e)

        to_be_deleted = self.SelectedNode()
        if to_be_deleted == None:
            return

        key = e.key()
        if key == Qt.Key_Delete:
            self.current_graph.RemoveNode(to_be_deleted.backendNode.guid)
            self.SetGraph(self.current_graph)

        # re-render after we have done anything here!
        self.viewport().update()
        codeString = self.genCmakeText()
        self.updateSignal.emit(codeString)

    def ClearAllSelections(self):
        for node in self._nodes:
            node.SetSelected(False)

    # There SHOULD always only be one selected node at a time
    def SelectedNode(self):
        for node in self._nodes:
            if node.isSelected:
                return node
        return None