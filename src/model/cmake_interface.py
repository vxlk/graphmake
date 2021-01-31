import cmd
from util.settings import *

class CMakeErrorWrapper():
    def __init__(self):
        error_list = []

# The interface to cmake from graphmake
# This class is responsible for:
# compiling cmake
# reporting results
class CMakeInterface():
    def __init__(self):
        # will probably need a handle to cmd
        # a path that is %CD%
        # an error class

        self.console = None
        self.current_dir = settings.cmakeFilePath # current directory
        self.error_wrapper = CMakeErrorWrapper()

    def Compile(self):
        self.Update()

    # Call this on init so we can report errors to the console
    def ConnectConsole(self, console):
        self.console = console

    # Called before every function to make sure we have the up to
    # date file location
    def Update(self):
        self.current_dir = os.path.dirname(settings.CmakeFile())
        