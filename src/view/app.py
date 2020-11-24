from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class TextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

class GraphEditor(QAbstractScrollArea):
    def __init__(self):
        super().__init__()
        self._nodes = []
    def mousePressEvent(self, e):
        self._nodes.append(e.pos())
        super().mousePressEvent(e)
        self.viewport().update()
    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self.viewport())
        for node in self._nodes:
            rect = QRect(node, QSize(100, 100))
            brush = QBrush(Qt.blue)
            rectF = QRectF(node.x(), node.y(), 100, 100)
            painter.fillRect(rectF, brush)
            painter.drawRect(rect)

app = QApplication([])

graph = GraphEditor()
text = TextEditor()

graphContainer = QDockWidget("Graph Container")
graphContainer.setAllowedAreas(Qt.LeftDockWidgetArea)
graphContainer.setWidget(graph)

textContainer = QDockWidget("Text Container")
textContainer.setAllowedAreas(Qt.RightDockWidgetArea)
textContainer.setWidget(text)
text.setPlainText("Click with the mouse below to shoot ;-)")

# The rest of the code is as for the normal version of the text editor.

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

window.show()
app.exec_()