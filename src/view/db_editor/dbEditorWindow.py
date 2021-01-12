from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.nodeSelector import *
from view.console import *

class XMLVarButton(QWidget):

    delete_me = pyqtSignal(object)

    def __init__(self, parent, name_str):
        super().__init__(parent)

        self.layout = QGridLayout(self)

        self.label = QLabel()
        self.label.setText(name_str)
        self.name = name_str
        self.layout.addWidget(self.label)

        self.var_input = QTextEdit(self)
        self.layout.addWidget(self.var_input)

        self.remove_var_button = QPushButton()
        self.remove_var_button.setText("Remove")
        self.remove_var_button.clicked.connect(lambda:self.removeSelf())
        self.layout.addWidget(self.remove_var_button)

        self.setLayout(self.layout)

    def removeSelf(self):
        #make a signal that emits here, the view widget
        #can pick this up, and then delete the button 
        #with the given name
        self.delete_me.emit(self.name)

class XMLViewWidget(QWidget):
    def __init__(self, parent, view_str_name, enable_append = False):
        super().__init__(parent)
        # todo: dynamic variables
        self.layout = QGridLayout(self)
        self.varNum = 1
        self.varButtons = []

        if enable_append == False:
            # Type
            # Func
            func_label = QLabel(self)
            func_label.setText(view_str_name)
            self.layout.addWidget(func_label)

            func_input = QTextEdit(self)
            self.layout.addWidget(func_input)

        else:
            # Var
            var_label = QLabel(self)
            var_label.setText("Variable")
            self.layout.addWidget(var_label)

            add_more_vars_button = QPushButton()
            add_more_vars_button.setText("Add Variable")
            add_more_vars_button.clicked.connect(lambda:self.AddVarButton())
            self.layout.addWidget(add_more_vars_button)
        
        self.setLayout(self.layout)

    def AddVarButton(self):
        var_button = XMLVarButton(self, "Variable " + str(self.varNum))
        var_button.delete_me.connect(self.onDelete)
        self.varNum += 1
        self.layout.addWidget(var_button)
        self.varButtons.append(var_button)

    @pyqtSlot(object)
    def onDelete(self, text):
        for var_button in self.varButtons:
            print(var_button.name)
            if var_button.name == text:
                print(var_button.name + "deleted")
                var_button.deleteLater()
                var_button = None
        

class DBEditorWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        layout = QGridLayout(self)

        func_widget = XMLViewWidget(self, "Function")
        layout.addWidget(func_widget)

        var_widget = XMLViewWidget(self, "Variable", True)

        scroll_area = QScrollArea()
        scroll_area.setWidget(var_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(scroll_area)

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
        