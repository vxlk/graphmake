from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.node import NodeWidget

class TextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        #self.setStyle("Fusion")
        # Now use a palette to switch to dark colors: (This no workie)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.viewport().setPalette(palette)

class GraphEditor(QAbstractScrollArea):
    def __init__(self):
        super().__init__()
        self._nodes = []

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
            painter.fillRect(node.asRectF(), node.brush())
            painter.drawRect(node.asRect())

# make Qapp
app = QApplication([])

# make the text and graph widgets themselves
graph = GraphEditor()
text = TextEditor()

# create dock widget "containers" for the text and graph widgets
graphContainer = QDockWidget("Graph Container")
graphContainer.setAllowedAreas(Qt.LeftDockWidgetArea)
graphContainer.setWidget(graph)

textContainer = QDockWidget("Text Container")
textContainer.setAllowedAreas(Qt.RightDockWidgetArea)
textContainer.setWidget(text)
text.setPlainText("Cmake text goes here..")

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

app.setApplicationName("Graphmake Alpha")
window = MainWindow()
window.addDockWidget(Qt.LeftDockWidgetArea, graphContainer)
window.addDockWidget(Qt.RightDockWidgetArea, textContainer)
file_path = None

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

# Force the style to be the same on all OSs:
app.setStyle("Fusion")

# Now use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)

app.setPalette(palette)

window.show()
app.exec_()