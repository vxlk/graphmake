# A graph is a backend representation of a connected graph of nodes and variables
class Graph():
    def __init__(self, name):
        self.nodes = []
        self.vars = []
        self.connections = {} # connections are indexed by <node array index> : [ var 1 , var 2 ... ]
        self.name = name

    def AddConnection(self, int_node_index, str_var):
        if int_node_index in self.connections:
            self.connections[int_node_index].append(str_var)
        else:
            self.connections[int_node_index] = [str_var]

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
        validator_flag = database.parser.Value(str_var_name) != database.parser.invalid_node
        if validator_flag:
            if connected_func_node_index != None:
                self.AddConnection(connected_func_node_index)
            else:
                self.vars.append(str_var_name)
        else:
            raise Exception('Could not find variable: ' + str_var_name + ' while parsing cmake file')
       
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