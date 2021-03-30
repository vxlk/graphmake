from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from util.settings import *
from view.graphEditor import GraphEditor
from view.textEditor import TextEditor
from view.nodeSelector import NodeSelectorTree
from view.console import Console
from view.db_editor.dbEditorWindow import *
from view.style_sheets.qss_style_collection import QssStyleSheetManager
from util.logger import *
from util.app_versioning import *
from model.cmake_parser import *
from model.cmake_interface import *

from functools import partial

# clear logs
logger.ClearLogs()
cmake_output_log.ClearLogs()

# make Qapp
app = QApplication([])

# make the text and graph widgets themselves
graph = GraphEditor()
graph.setMinimumSize(512, 512)

text = TextEditor()
text.setMinimumSize(212, 212)
text.connectGraph(graph)

nodeTree = NodeSelectorTree("Function") # todo: rename to specify this is the function tree
nodeTree.Widget().setMinimumSize(212, 600)
nodeTree.setMinimumSize(212, 212)
nodeTreeVar = NodeSelectorTree("Variable")
nodeTreeVar.Widget().setMinimumSize(212, 600)
nodeTreeVar.setMinimumSize(212, 212)
nodeTree.filterSignal.connect(nodeTreeVar.onFilterEvent)

console = Console()
console.connectLog(cmake_output_log)

# create dock widget "containers" for the text and graph widgets
graphContainer = QDockWidget(settings.cmakeFilePath)
graphContainer.setAllowedAreas(Qt.LeftDockWidgetArea)
graphContainer.setWidget(graph)

textContainer = QDockWidget("Cmake Text")
textContainer.setAllowedAreas(Qt.RightDockWidgetArea)
textContainer.setWidget(text)

nodeSelectorContainer = QDockWidget("Functions")
nodeSelectorContainer.setAllowedAreas(Qt.LeftDockWidgetArea) 
nodeSelectorContainer.setWidget(nodeTree)

nodeSelectorContainerVar = QDockWidget("Variables")
nodeSelectorContainerVar.setAllowedAreas(Qt.LeftDockWidgetArea) 
nodeSelectorContainerVar.setWidget(nodeTreeVar)

consoleContainer = QDockWidget("Console")
consoleContainer.setAllowedAreas(Qt.BottomDockWidgetArea)
consoleContainer.setWidget(console)

# code for the app itself
class MainWindow(QMainWindow):
    def closeEvent(self, e):
        if not text.document().isModified():
            return
        answer = QMessageBox.question(
            window, None,
            "You have unsaved changes. Save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        if answer & QMessageBox.Save:
            save()
        elif answer & QMessageBox.Cancel:
            e.ignore()

app.setApplicationName("Graphmake " + app_version)
window = MainWindow()

window.addDockWidget(Qt.LeftDockWidgetArea, graphContainer)
window.addDockWidget(Qt.RightDockWidgetArea, textContainer)
window.addDockWidget(Qt.LeftDockWidgetArea, nodeSelectorContainer)
window.splitDockWidget(nodeSelectorContainer, graphContainer, Qt.Horizontal)
window.splitDockWidget(nodeSelectorContainer, nodeSelectorContainerVar, Qt.Horizontal)
window.addDockWidget(Qt.BottomDockWidgetArea, consoleContainer)

file_path = settings.Value(settings.kCmakeFileLoc)

menu = window.menuBar().addMenu("&File")
open_action = QAction("&Open")
def open_file():
    global file_path
    path = QFileDialog.getOpenFileName(window, "Open")[0]
    if path:
        text.setPlainText(open(path).read())
        file_path = path
open_action.triggered.connect(open_file)
open_action.setShortcut(QKeySequence.Open)
menu.addAction(open_action)

app_settings = window.menuBar().addMenu("&Settings")
theme_menu = app_settings.addMenu("&Theme")

actions = []
index = 0

def set_css_style(style_name : str) -> None:
    settings.Add(settings.kThemeColor, style_name)
    QssStyleSheetManager.currently_selected = style_name
    # Force update
    app.setStyleSheet(QssStyleSheetManager.collection[style_name])
    for action in actions:
        action.setChecked(False)
        if action.objectName() == style_name:
            action.setChecked(True)

for item in QssStyleSheetManager.collection.keys():
    # no duplicates please
    if item in actions:
        continue
    actions.append(QAction(item))
    actions[index].setCheckable(True)
    actions[index].setObjectName(item)
    if (item == QssStyleSheetManager.currently_selected):
        actions[index].setChecked(True)
    actions[index].triggered.connect(partial(set_css_style, item))
    theme_menu.addAction(actions[index])
    index +=1

save_action = QAction("&Save")
def save():
    if file_path is None:
        save_as()
    else:
        with open(file_path, "w") as f:
            f.write(text.toPlainText())
        text.document().setModified(False)
save_action.triggered.connect(save)
save_action.setShortcut(QKeySequence.Save)
menu.addAction(save_action)

save_as_action = QAction("Save &As...")
def save_as():
    global file_path
    path = QFileDialog.getSaveFileName(window, "Save As")[0]
    if path:
        file_path = path
        save()
save_as_action.triggered.connect(save_as)
menu.addAction(save_as_action)                                                                                          

close = QAction("&Close")
close.triggered.connect(window.close)
menu.addAction(close)

help_menu = window.menuBar().addMenu("&Help")
about_action = QAction("&About")
help_menu.addAction(about_action)
def show_about_dialog():
    text = "<center>" \
           "<h1>Text Editor</h1>" \
           "&#8291;" \
           "<img src=icon.svg>" \
           "</center>" \
           "<p>Version 31.4.159.265358<br/>" \
           "Copyright &copy; Company Inc.</p>"
    QMessageBox.about(window, "About Text Editor", text)
about_action.triggered.connect(show_about_dialog)

# --- Database Editor Window --- #

db_editor = window.menuBar().addMenu("&Database Editor")
db_editor_action = QAction("&Open")
db_editor.addAction(db_editor_action)

editor_widget = DBEditorWindow() # no parent is questionable
editor_widget.connectConsole(console, logger)
editor_widget.hide()

def show_editor_widget():
    # writing it in this way to leave room for expansion in the case that this requires more set
    # up in the future
    editor_widget.show()
db_editor_action.triggered.connect(show_editor_widget)

# --- Database Editor Window --- #

# --- CMake Parser --- #

cmake_parser_button = window.menuBar().addMenu("&Open CMake File")
cmake_parser_action = QAction("&Open CMake File")
cmake_parser_button.addAction(cmake_parser_action)
cmake_parser = CMakeParser()
cmake_interface = CMakeInterface()
cmake_interface.ConnectConsole(console)
def open_cmake_file():
    cmake_file_path = QFileDialog.getOpenFileName(window, "Open")[0]
    if cmake_file_path:
        cmake_parser.OpenFile(cmake_file_path)
        # switch the cmake file to the new file in our settings when one is opened
        # Also update the settings file which i hate for now
        settings.cmakeFilePath = cmake_file_path
        # update dock widget's path
        graphContainer.setWindowTitle(settings.cmakeFilePath)
        settings.Add(settings.kCmakeFileLoc, cmake_file_path)
        # update our text view with the contents of the new cmake file
        with open (cmake_file_path, "r") as cmake_file:
            data_list = cmake_file.readlines()
            graph.SetGraph(cmake_parser.GenerateGraph(data_list))
                    
cmake_parser_action.triggered.connect(open_cmake_file)

# --- CMake Parser --- #

# --- CMake Compiler --- #
cmake_compiler_button = window.menuBar().addMenu("&Compile")
cmake_compiler_action = QAction("&Run")
cmake_compiler_button.addAction(cmake_compiler_action)

def compile_cmake_file():
    cmake_interface.Compile()

cmake_compiler_action.triggered.connect(compile_cmake_file)
# --- CMake Compiler --- #

# Force the style to be the same on all OSs:
app.setStyleSheet(QssStyleSheetManager.collection[QssStyleSheetManager.currently_selected])

# Now use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)

app.setPalette(palette)

window.show()
app.exec_()