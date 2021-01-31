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
    def Left(self):
        return self.neighbor_left
    def Right(self):
        return self.neighbor_right

    # retrieve the payload (in this case a string)
    def Data(self):
        return self.xml_node_name

# A specific level in the @LevelList
class Level():
    def __init__(self, int_level_num):
        self.nodes = [] # a list of nodes at the level
        self.level_num = int_level_num
        self.iterator = 0

    # First node in the level -> resets the iterator
    def First(self):
        self.iterator = 0
        if len(self.nodes) > 0:
            return self.nodes[0]
        return None

    # Next node in the level
    def Next(self):
        self.iterator += 1
        if self.LastNodeNum() > self.iterator:
            return self.nodes[self.iterator]
        return None

    # The previous node in the level
    def Prev(self):
        if self.LastNodeNum() > self.iterator:
            return self.nodes[self.iterator].Prev()
        return None
    
    # The last node in the level
    def Last(self):
        index = len(self.nodes)
        if index == 0:
            return None
        return self.nodes[index-1]

    # Number of the last node in the level
    def LastNodeNum(self):
        return len(self.nodes)

    # assume parent/child is set before inserting into the level
    # Insert a node into this level -> done internally through levelList -> not designed to be called directly
    def Insert(self, node):
        # assign neighbors
        last_node = self.Last()
        if last_node != None:
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
# todo: ascii art drawing so this makes sense
class LevelList():
    def __init__(self):
        self.levels = []
        self.iterator = 0

    # 0 indexing
    # add a node to a certain level
    # if that level does not exist it will be made
    # assumes everything that comes in will be in the order that you want
    # the nodes to be in
    def AddNode(self, str_name, int_level):
        if int_level > len(self.levels)-1:
            self.AddNewLevel(str_name)
        else:
            self.AddToCurrentLevel(str_name, int_level)
    
    # internal function from add node
    def AddNewLevel(self, str_name):
        prev_level = self.LastLevel()
        self.levels.append(Level(self.LastLevelNum() + 1))
        current_level = self.LastLevel()
   
        new_node = LevelNode()
        new_node.xml_node_name = str_name
        current_level.Insert(new_node)

        if prev_level != None:
           current_level.Last().parent = prev_level.Last()
           prev_level.Last().child = current_level.Last()
           debug_parent_name = prev_level.Last().Data()
           prev_level.Last().child = current_level.Last()

    # internal function from add node
    def AddToCurrentLevel(self, str_name, int_level):
        current_level = self.levels[int_level]
        node = LevelNode()
        # figure out parent
       
        # if we arent at the root level, go up one - else no parent
        if (int_level-1 >= 0):
            node.parent = self.levels[int_level-1].Last()
            self.levels[int_level-1].Last().child = node
        else:
            node.parent = None

        #last_level.child = node
        node.xml_node_name = str_name
        current_level.Insert(node)
    
    # Return the last level in the list -> all iteration goes backwards
    def LastLevel(self):
        if len(self.levels) > 0:
            return self.levels[len(self.levels)-1]
        return None

    # number of the last level
    def LastLevelNum(self):
        return len(self.levels)

    # Get the next level in the list
    def Next(self):
        self.iterator += 1
        if self.LastLevelNum() > self.iterator:
            return self.levels[self.iterator]
        return None

    # Get the previous level in the list
    def Prev(self):
        prev_iter = self.iterator - 1
        if prev_iter >= 0:
            return self.levels[prev_iter]
        return None

    # Get the first level in the list and reset the iterator
    def FirstLevel(self):
        self.iterator = 0
        if self.LastLevel != None:
            return self.levels[0]
        else:
            return None
    
    # return the number held by the internal iterator
    def CurrentLevelNum(self):
        return self.iterator
    
    # assumes you checked this, return the level @ number -> DOES NOT BOUNDS CHECK
    def CurrentLevel(self):
        return self.levels[self.iterator]

    # Find a node anywhere in the list -> empty node returned if not found
    def FindNode(self, str_node_name):
        level = self.FirstLevel()
        while level != None:
            node = level.First()
            while node != None:
                if str_node_name == node.Data():
                    return node
                node = level.Next()
            level = self.Next()
        return None

    # Print the list for debugging -> also a good example of how the scuffed iterators work
    def Print(self):
        level = self.FirstLevel()
        while level != None:
            node = level.First()
            print("Level: ")
            print(level.level_num)
            while node != None:
                parent = ""
                child = ""
                if node.Up() != None:
                    parent = node.Up().Data()
                if node.Down() != None:
                    child = node.Down().Data()
                print(node.Data() + " Parent: " + parent + " Child: " + child)
                node = level.Next()

            level = self.Next()

# 0 - global_cmake --------------------
#        |  child()          |            |
# 1 - cmake_version,       next() global_set, scripting
#     parent() ^| child()             |           |
# 2 - var1 var2                    var1 var2   var1 var2