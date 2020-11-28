
# a connection represents a "connection" between 2 nodes
# (node a. and node b.) a. will have an output and b. will
# have an input.  output can be piped into input, this cannot
# be done the other way
# a variable definition will always have an output (that can be
# the input to many different nodes)
from PyQt5.QtCore import * 
import uuid

class Pin:
    def __init__(self, isInput = False):
        self.node_guid = None
        self.guid = uuid.uuid4()
        self.connection_guids = []
        self.name = "Input" if isInput else "Output"
        self.code = ""
        self.num_conns = 0
        self.max_num_cons = 1
        self.isInput = isInput

    def _type(self):
        return "Input" if self.isInput else "Output"

    def connected(self):
        #return find node for each id
        return self.connection_guids

def create_input_pin():
    return Pin(True)
def create_output_pin():
    return Pin()

        