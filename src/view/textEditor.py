from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.settings import *

class TextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.text = ""

    def connectGraph(self, graphEditor):
        graphEditor.updateSignal.connect(self.onGraphUpdate)

    @pyqtSlot(object)
    def onGraphUpdate(self, text):
        self.text = text
        self.setPlainText(text)
        self.auto_save()

    def auto_save(self):
        file_path = settings.Value(settings.kCmakeFileLoc)
        if file_path is None:
            print("Auto save error - cmake file doesn't exist")
            return
        else:
            with open(file_path, "w+") as f:
                f.write(self.text)
            self.document().setModified(False)