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

    # retrieve the payload (in this case a string)
    def Data(self):
        self.xml_node_name

# A specific level in the @LevelList
class Level():
    def __init__(self, int_level_num):
        self.nodes = [] # a list of nodes at the level
        self.level_num = int_level_num
        self.iterator = 0

    def First(self):
        if len(self.nodes) > 0:
            return self.nodes[0]
        return None

    def Next(self):
        self.iterator += 1
        if self.Last() < iterator:
            return self.nodes[self.iterator]
        return None

    def Prev(self):
        if self.Last() < iterator:
            return self.nodes[self.iterator].Prev()
        return None
    
    def Last(self):
        index = len(self.nodes)
        if index == 0:
            return None
        return self.nodes[index-1]

    def LastLevel(self):
        if len(self.nodes) > 0:
            return self.nodes[len(self.nodes)-1]
        return None

    def LastLevelNum(self):
        return len(self.levels)

    # assume parent/child is set before inserting into the level
    def Insert(self, node):
        # assign neighbors
        last_node = self.Last()
        last_node.neighbor_right = node
        node.neighbor_left = last_node
        # add to the list now that the neighbors are assigned
        self.nodes.append(node)

# A level list is a data structure that is meant to mirror the structure of xml in code
# it provides:
# a numbered level
# a list of nodes at that level
# a list of children under that node with their appropriate levels
#
# During construction: assumes all nodes added are in order that they should be in the tree
# Supports:
# A
class LevelList():
    def __init__(self):
        self.levels = []
        self.iterator = 0

    # 0 indexing idiot
    def AddNode(self, str_name, int_level):
        if int_level > len(self.levels)-1:
            self.AddNewLevel(str_name)
        else:
            self.AddToCurrentLevel(str_name, int_level)

    def AddNewLevel(self, str_name):
        self.levels.append(Level(self.LastLevelNum() + 1))
        current_level = self.LastLevel()
        current_level.parent = self.LastLevel()  
        self.LastLevel().child = current_level
        current_level.xml_node_name = str_name

    def AddToCurrentLevel(self, str_name, int_level):
        current_level = self.levels[int_level]
        node = LevelNode()
        # figure out parent
        last_level = self.LastLevel()
        node.parent = last_level.Last()
        last_level.child = node
        current_level.Insert(node)
        current_level.xml_node_name = str_name
        
    def LastLevel(self):
        if len(self.levels) > 0:
            return self.levels[len(self.levels)-1]
        return None

    def LastLevelNum(self):
        return len(self.levels)

    def Next(self):
        self.iterator += 1
        if self.LastLevelNum() < iterator:
            return self.levels[self.iterator]
        return None

    def Prev(self):
        prev_iter = self.iterator - 1
        if prev_iter >= 0:
            return self.levels[prev_iter]
        return None

    def FirstLevel(self):
        self.iterator = 0
        if self.LastLevel != None:
            return self.levels[0]
        else:
            return None
    
    def CurrentLevelNum(self):
        return self.iterator
    
    # assumes you checked this
    def CurrentLevel(self):
        return self.levels[self.iterator]

# 0 - global_cmake --------------------
#        |  child()          |            |
# 1 - cmake_version,       next() global_set, scripting
#     parent() ^| child()             |           |
# 2 - var1 var2                    var1 var2   var1 var2