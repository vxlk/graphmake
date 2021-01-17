from view.node import *
from model.node import *
# the main controller module that acts as a wrapper around the model and view
# will enable behavior that syncronizes actions from function calls

class Controller:
    def __init__(self):
        self.modelNodes = []
        self.guiNodes = [] #for now keep track of nodes directly, eventually move this to graphs
    
    def CurrentNodeName(self):
        return nodeSelector.CurrentNodeName()

controller = Controller()
