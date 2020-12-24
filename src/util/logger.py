from util.settings import *

#todo: error logging
class Logger():
    def __init__(self):
        self.contents = ''

    def filePath(self):
        settings.Value(settings.kLogFileLoc)