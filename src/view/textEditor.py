from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        #self.setStyle("Fusion")
        # Now use a palette to switch to dark colors: (This no workie)
        #palette = QPalette()
        #palette.setColor(QPalette.Window, QColor(53, 53, 53))
        #palette.setColor(QPalette.WindowText, Qt.white)
        #self.viewport().setPalette(palette)
        self.text = ""

    def connectGraph(self, graphEditor):
        graphEditor.updateSignal.connect(self.onGraphUpdate)

    @pyqtSlot(object)
    def onGraphUpdate(self, text):
        self.text = text
        self.setPlainText(text)