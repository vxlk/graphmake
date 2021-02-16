from model.db.db_module.db_model import *
from model.node_model import *
import uuid

# a small container that represents a node in a graph
# devoid of concerns of ui or really any functionality,
# this has the job of keeping track of the name and a unique
# indentifier (since all info can be retrieved from just a name, and the 
# uid keeps names unique)
class GraphNode():
    def __init__(self, str_node_name):
        self.guid = uuid.uuid4()
        self.name = str_node_name
        self.x = 0
        self.y = 0

    def HasPosition(self):
        return self.x and self.y # kinda neat looking but this checks that they both arent 0

# A graph is a backend representation of a connected graph of nodes and variables
class Graph():
    def __init__(self, name):
        self.nodes = [] # list of strings of names of function nodes
        self.vars = []  # list of strings of names of variable nodes
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
    def TryAddVar(self, str_var_name, connected_func_node_index = None, x_pos = 0, y_pos = 0):
        # validate node
        # if connected:
        # add to connections list
        # else:
        # add to vars list
        database.parser.SetMode(database.parser.varMode)
        var_name = database.parser.ValueName(str_var_name)
        validator_flag = var_name != database.parser.invalid_node
        if validator_flag:
            new_node = GraphNode(str_var_name)
            new_node.x = x_pos
            new_node.y = y_pos 

            self.vars.append(new_node)
            curr_var_index = len(self.vars) - 1
            
            if connected_func_node_index != None:
                self.AddConnection(connected_func_node_index, curr_var_index)

            return new_node.guid
        else:
            #raise Exception('Could not find variable: ' + str_var_name + ' while parsing cmake file')
            print('Could not find variable: ' + str_var_name + ' while parsing cmake file')
            return nodeManager.bad_node_guid

    # Should eventually check to make sure the function node being added is valid...
    def TryAddNode(self, str_node_name, x_pos = 0, y_pos = 0):
        new_node = GraphNode(str_node_name)
        new_node.x = x_pos
        new_node.y = y_pos 
        self.nodes.append(new_node)
        return new_node.guid
        

    # given guid, remove the node from the graph - this is written like c-code and i dont really care
    # dont @ me
    def RemoveNode(self, guid):
        index = 0
        node_index_to_be_deleted = -1
        connection_index_to_be_deleted = -1
        var_index_to_be_deleted = -1
        for node in self.nodes:
            if node.guid == guid:
                # delete the node
                node_index_to_be_deleted = index
                # delete it in the connections
                for connection_key in self.connections.keys():
                    if connection_key == node_index_to_be_deleted:
                        connection_index_to_be_deleted = connection_key
                    else:
                        connection_index_to_be_deleted += 1
                break # stop counting
            else:
                index += 1

        if node_index_to_be_deleted != -1:
            self.nodes.remove(self.nodes[node_index_to_be_deleted])
            if connection_index_to_be_deleted != -1:
                self.connections.pop(self.connections[connection_index_to_be_deleted])
            return # avoid looking in the other container

        index = 0
        # check variables if we have to
        for var in self.vars:
            if var.guid == guid:
                var_index_to_be_deleted = index
                break
            else:
                index += 1

        if var_index_to_be_deleted != -1:
            self.vars.remove(self.vars[var_index_to_be_deleted])
        else:
            raise Exception("Did not find the node we were trying to delete: guid " + str(guid))
                
                

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