
# A specific node in a @Level
class LevelNode():
    def __init__(self):
        self.xml_node_name = ""
        self.level_num = 0
        
        # how we traverse the chain
        self.parent = None
        self.child = None
        self.neighbor_left = None
        self.neighbor_right = None

    def Down(self):
        return self.child
    def Up(self):
        return self.parent
    def Next(self):
        return self.neighbor_left
    def Prev(self):
        return self.neighbor_right

# A specific level in the @LevelList
class Level():
    def __init__(self):
        self.nodes = [] # a list of nodes at the level
        self.level_num = 0

    def First(self):
        if len(self.nodes) > 0:
            return self.nodes[0]
        return None

    def Insert(self):
        # todo
        self.nodes.append(None)

# A level list is a data structure that is meant to mirror the structure of xml in code
# it provides:
# a numbered level
# a list of nodes at that level
# a list of children under that node with their appropriate levels
#
# Supports:
# GetNodesAtLevel()
# GetChildren()
# GetParents()
# GetNode()
class LevelList():
    def __init__(self):
        self.levels = []