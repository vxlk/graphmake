import cmd
from util.settings import *
from util.logger import *

# not currently used but will be useful in providing error tips
class CMakeErrorWrapper():
    def __init__(self):
        error_list = []

# The interface to cmake from graphmake
# This class is responsible for:
# compiling cmake
# reporting results
class CMakeInterface():
    def __init__(self):
        self.console = None
        self.current_dir = settings.cmakeFilePath # current directory
        self.error_wrapper = CMakeErrorWrapper()

    # extremely not sophisticated
    # todo: revisit and add some features here
    def Compile(self):
        self.Update()

        og_dir = os.getcwd()
        os.chdir(self.current_dir)
        stream = os.popen('cmake .')
        output = stream.read()
        logger.Log(output)
        os.chdir(og_dir)

    # Call this on init so we can report errors to the console
    def ConnectConsole(self, console):
        self.console = console

    # Called before every function to make sure we have the up to
    # date file location
    def Update(self):
        self.current_dir = os.path.dirname(settings.cmakeFilePath)
        