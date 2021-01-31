from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.graphEditor import GraphEditor
from view.textEditor import TextEditor
from view.nodeSelector import NodeSelectorTree
from view.console import Console
from view.db_editor.dbEditorWindow import *
from util.settings import *
from util.logger import *

# graphmake version number
# -------------------------------
# Release . Major . Minor . Patch
# -------------------------------
# Release - [Internal, Alpha, Beta, Release]
#            Interal - A build for internal use from (graphmake) developers only
#            Alpha - A build given to a select group for testing
#            Beta - A build given to the mass audience for testing
#            Release - A trusted build that can be given to any client
# Major - Indicates a fundamental change in how the application works
# Minor - Indicates a new release to the public, a group of patches applied/features added
# Patch - An update that feels meaningful
version_number = "Alpha.0.0.1"

# clear logs
logger.ClearLogs()

# make Qapp
app = QApplication([])

# make the text and graph widgets themselves
graph = GraphEditor()
graph.setMinimumSize(512, 512)
text = TextEditor()
text.setMinimumSize(212, 212)
text.connectGraph(graph)
nodeTree = NodeSelectorTree("Function") # todo: rename to specify this is the function tree
nodeTree.Widget().setMinimumSize(212, 212)
nodeTreeVar = NodeSelectorTree("Variable")
nodeTreeVar.Widget().setMinimumSize(212, 212)
console = Console()
console.connectLog(logger) # this could probably be reworked (depending on how we handle cmake entry)

# create dock widget "containers" for the text and graph widgets
graphContainer = QDockWidget("Graph Container")
graphContainer.setAllowedAreas(Qt.LeftDockWidgetArea)
graphContainer.setWidget(graph)

textContainer = QDockWidget("Text Container")
textContainer.setAllowedAreas(Qt.RightDockWidgetArea)
textContainer.setWidget(text)

nodeSelectorContainer = QDockWidget("Functions")
nodeSelectorContainer.setAllowedAreas(Qt.LeftDockWidgetArea) 
nodeSelectorContainer.setWidget(nodeTree.Widget())

nodeSelectorContainerVar = QDockWidget("Variables")
nodeSelectorContainerVar.setAllowedAreas(Qt.LeftDockWidgetArea) 
nodeSelectorContainerVar.setWidget(nodeTreeVar.Widget())

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

app.setApplicationName("Graphmake " + version_number)
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

# Force the style to be the same on all OSs:
app.setStyle("Fusion")

# Now use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)

app.setPalette(palette)

window.show()
app.exec_()