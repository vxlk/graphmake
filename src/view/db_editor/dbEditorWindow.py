from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.nodeSelector import *

class DBEditorWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

class DBEditorWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setMinimumSize(QSize(400,400))
        self.setWindowTitle("Database Editor")
        
        self.selectorContainer = QDockWidget()
        self.nodeSelector = NodeSelectorTree()
        self.selectorContainer.setWidget(self.nodeSelector.Widget())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.selectorContainer)

        self.db_editorContainer = QDockWidget()
        self.db_editor = DBEditorWidget()
        self.db_editorContainer.setWidget(self.db_editor)
        self.addDockWidget(Qt.RightDockWidgetArea, self.db_editorContainer)
        