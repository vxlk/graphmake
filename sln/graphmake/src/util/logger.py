from PyQt5.QtCore import *
from util.settings import *
import datetime
import sys

#todo: error logging
class Logger(QObject):
    
    updateSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.contents = ''

        # types of log messages
        self.critical = "CRITICAL: "
        self.error = "ERROR: "
        self.normal = ""

    def FilePath(self):
        return settings.Value(settings.kLogFileLoc)

    def Log(self, msg, func_name = "", _type = ""):
        if func_name == "":
            func_name = sys._getframe(1).f_code.co_name
        self.contents += (str(datetime.datetime.now()) + 
                          " " + (_type + " {FUNCTION}:"  + func_name + " {MESSAGE}:" + str(msg))) + "\n"
        with open(self.FilePath(), "w+") as f:
                f.write(self.contents)
                f.close()
        self.updateSignal.emit(self.contents)

    def ClearLogs(self):
        with open(self.FilePath(), "w+") as f:
            f.write("")
            f.close()

# global instance
logger = Logger()
