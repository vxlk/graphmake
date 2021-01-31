import re
# A holding structure for the parser while parsing
# will contain a directed graph of string names of:
# nodes
# vars
# connections between the two
class CMakeData():
    def __init__(self):
        self.nodes = []
        self.vars = []
        self.connections = {}

    def AddConnection(self, str_node, str_var):
        crap = None

    # Try to find a match in the database using reverse lookup - if it is a hit
    # add it to the variable list
    # Reallistically should be doing the same for nodes but it is not necessary right now
    def TryAddVar(self, str_var_name, connected_func_node = ""):
        crap = None
        
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
    def GenerateGraph(self, text_line_by_line, graphEditor):
        for line in text_line_by_line:
            # not ideal
            split_line = re.split(r'[(,\s]\s*', line)

            # NO BOUNDS CHECKS YOLO
            # add function
            self.data.nodes.append(split_line[0])

            # sanitize out unneeded end parenthesis
            for split in split_line:
                split = split.replace(')', '')
                self.data.TryAddVar(split, split_line[0])

            # split_line[0] = function
            # split_line[n] is each POTENTIAL variable -> parse and try to find a match?
            i = 0
        