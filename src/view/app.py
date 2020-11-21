import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#todo: think about decoupling the main window from the app itself

app = QApplication(sys.argv)

#retrive main window instance
mainWindow = QMainWindow()
mainWindow.setWindowTitle("Graphmake alpha")

#populate window data here
graph = QWidget(mainWindow)
graph.setMinimumWidth(800)
graph.setMinimumHeight(600)

#use qpainter to draw rectangle
node = QWidget(graph)
node.setMinimumWidth(100)
node.setMinimumHeight(100)
nodePalette = node.palette()
nodePalette.setColor(node.backgroundRole(), Qt.blue)
node.setPalette(nodePalette)
node.show()
print(node.pos().x())

#finish rendering background for graph
graphPalette = graph.palette()
graphPalette.setColor(graph.backgroundRole(), Qt.red)
graph.setPalette(graphPalette)
graph.show()

mainWindow.setCentralWidget(graph)
mainWindow.show()

app.exec_()
