from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.settings import *

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

    def auto_save(self):
        file_path = settings.Value(settings.kCmakeLoc)
        if file_path is None:
            print("Auto save error - cmake file doesn't exist")
            return
        else:
            with open(file_path, "w") as f:
                f.write(text.toPlainText())
            self.document().setModified(False)