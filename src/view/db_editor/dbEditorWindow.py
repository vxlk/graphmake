from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.nodeSelector import *
from view.console import *

class XMLViewWidget(QWidget):
    def __init__(self, parent, view_str_name, enable_append = False):
        super().__init__(parent)
        # todo: dynamic variables
        layout = QGridLayout(self)

        if enable_append == False:
            # Type
            # Func
            func_label = QLabel(self)
            func_label.setText(view_str_name)
            layout.addWidget(func_label)

            func_input = QTextEdit(self)
            layout.addWidget(func_input)

        else:
            # Var
            var_label = QLabel(self)
            var_label.setText("Variable")
            layout.addWidget(var_label)

            var_input = QTextEdit(self)
            layout.addWidget(var_input)

            add_more_vars_button = QPushButton()
            add_more_vars_button.setText("Add")
            layout.addWidget(add_more_vars_button)

            remove_var_button = QPushButton()
            remove_var_button.setText("Remove")
            layout.addWidget(remove_var_button)

class DBEditorWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        layout = QGridLayout(self)

        func_widget = XMLViewWidget(self, "Function")
        layout.addWidget(func_widget)

        var_widget = XMLViewWidget(self, "Variable", True)
        layout.addWidget(var_widget)

        insert_button = QPushButton()
        insert_button.setText("Insert Into Database")
        layout.addWidget(insert_button)

        # Fields

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

    def connectConsole(self, console, logger):
        editor_console = Console()
        editor_console.text = console.text
        editor_console.connectLog(logger)
        consoleContainer = QDockWidget()
        consoleContainer.setWidget(editor_console)
        self.addDockWidget(Qt.BottomDockWidgetArea, consoleContainer)
        