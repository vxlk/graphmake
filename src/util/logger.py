from util.settings import *
import datetime

#todo: error logging
class Logger():
    def __init__(self):
        self.contents = ''

        # types of log messages
        self.critical = "CRITICAL:"
        self.error = "ERROR:"
        self.normal = ""

    def FilePath(self):
        return settings.Value(settings.kLogFileLoc)

    def Log(self, msg, _type = ""):
        self.contents += (str(datetime.datetime.now()) + 
                          " " + (_type + msg)) + "\n"
        with open(self.FilePath(), "w+") as f:
                f.write(self.contents)

    def ClearLogs(self):
        with open(self.FilePath(), "w+") as f:
            f.write("")

# global instance
logger = Logger()