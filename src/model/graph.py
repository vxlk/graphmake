from model.db.db_module.db_model import *
import uuid

# CRAP  CRAP CRAP MAKE A GRAPH NODE STRUCT
# MAKE NODES AUTO SELECT WHEN PLACED PLEASE

# A graph is a backend representation of a connected graph of nodes and variables
class Graph():
    def __init__(self, name):
        self.nodes = [] # list of strings of names of function nodes
        self.node_guids = [] # list of guids for func nodes
        self.vars = []  # list of strings of names of variable nodes
        self.var_guids = [] # list of guids for var nodes
        self.connections = {} # connections are indexed by <node array index> : [ var 1 , var 2 ... ]
        self.name = name

    def AddConnection(self, int_node_index, int_var_index):
        if int_node_index in self.connections:
            self.connections[int_node_index].append(int_var_index)
        else:
            self.connections[int_node_index] = [int_var_index]

    # Try to find a match in the database using reverse lookup - if it is a hit
    # add it to the variable list
    # Reallistically should be doing the same for nodes but it is not necessary right now
    # Limitation right now: WILL NOT CHECK THAT THE CONNECTION IS VALID WILL INSTEAD BY DEFAULT MAKE IT
    # in the future: allow invalid nodes as unrecognized editable fields
    def TryAddVar(self, str_var_name, connected_func_node_index = None):
        # validate node
        # if connected:
        # add to connections list
        # else:
        # add to vars list
        database.parser.SetMode(database.parser.varMode)
        var_name = database.parser.ValueName(str_var_name)
        validator_flag = var_name != database.parser.invalid_node
        if validator_flag:
            self.vars.append(var_name)
            self.var_guids.append(uuid.uuid4())
            curr_var_index = len(self.vars) - 1
            if connected_func_node_index != None:
                self.AddConnection(connected_func_node_index, curr_var_index)
              
        else:
            #raise Exception('Could not find variable: ' + str_var_name + ' while parsing cmake file')
            print('Could not find variable: ' + str_var_name + ' while parsing cmake file')

    # Should eventually check to make sure the function node being added is valid...
    def TryAddNode(self, str_node_name):
        self.nodes.append(str_node_name)
        self.node_guids.append(uuid.uuid64())

    def RemoveNode(self, guid):
        index = 0
        for node in self.node_guids:
            if node == guid:
                

    # THESE STILL ARENT UNIQUE!!!! TODO TODO USE GUIDS
    def NodeIndex(self, str_node_name):
        index = 0
        for node in self.nodes:
            if node == str_node_name:
                return index
            index += 1
        return -1 # meh

    def VarIndex(self, str_node_name):
        index = 0
        for node in self.vars:
            if node == str_node_name:
                return index
            index += 1
        return -1 # meh
       
# Contains every graph in the scene, queriable by name
class GraphManager():
    def __init__(self):
        self.graphs = {} # a graph is a dictionary of graph names : graph
        self.graphs['Root'] = Graph('Root')

    # Returns the root graph 
    def TopLevelGraph(self):
        return self.graphs['Root']

    # Return a graph given a name
    def Graph(self, str_name):
        if str_name in self.graphs:
            return self.graphs[str_name]
        return None

    def NewGraph(self, str_name = 'Root'):
        self.graphs[str_name] = Graph(str_name)
        return self.graphs[str_name]

graphManager = GraphManager()