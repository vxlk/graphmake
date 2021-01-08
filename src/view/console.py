from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from util.settings import *
from util.logger import *

# a simple debugging console for now, eventually i wanna do some kind of intellisense
# or something more useful, for now this will prove invaulable for debugging speeds

class Console(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.text = ""

    # this could probably be reworked depending on whether i want manual writing in the cmake
    def connectGraph(self, graphEditor):
        graphEditor.updateSignal.connect(self.onUpdate)

    def connectLog(self, log):
        log.updateSignal.connect(self.onUpdate)

    @pyqtSlot(object)
    def onUpdate(self, text):
        # check settings file
        log_file = open(logger.FilePath(), "r")
        self.text = log_file.read()
        self.setPlainText(self.text)
        log_file.close()