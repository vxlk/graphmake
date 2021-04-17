import re
from model.db.db_module.db_model import *
from model.graph import *

# A holding structure for the parser while parsing
# will contain a directed graph of string names of:
# nodes
# vars
# connections between the two
class CMakeData():
    def __init__(self):
        self.graph = graphManager.NewGraph() # make a new root graph
        
# A class responsible for parsing a cmake file,
# creating a cmake model,
# and giving the gui information to display
# this will report syntax errors and eventually contain the intellisense
class CMakeParser():
    def __init__(self):
        self.file_path = ""
        self.data = CMakeData()

    def OpenFile(self, path):
        self.file_path = path

    # take a text string for now but idk if thats how i wanna keep it
    def GenerateGraph(self, text_line_by_line):
        node_index = 0
        for line in text_line_by_line:
            # not ideal
            split_line = re.split(r'[(,\s]\s*', line)

            # NO BOUNDS CHECKS YOLO
            # add function
            self.data.graph.TryAddNode(split_line[0])
            node_index += 1

            # sanitize out unneeded end parenthesis
            for split in split_line:
                split = split.replace(')', '')
                self.data.graph.TryAddVar(split, self.data.graph.NodeIndex(split_line[0]))

            # split_line[0] = function
            # split_line[n] is each POTENTIAL variable -> parse and try to find a match?
        return self.data.graph
        