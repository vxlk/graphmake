from view.graphEditor import GraphEditor
from model.cmake_parser import *
from model.cmake_interface import *
from model.db.db_module.db_model import *
from model.node_model import *
from util.utilities import *

# A non gui way to interact with graphmake
# incapsulates its logic in a way that can be
# run from an external python script
# Use case:
#   Unit Testing
class ScriptingEngine(object):
    def __init__(self):
        self.graph = GraphEditor()
        self.cmake_parser = CMakeParser()
        self.cmake_compiler = CMakeInterface()
        self.db = Database()

    # will not support multiple graphs for now
    def add_node(self, node_name : str) -> None:
        guid = self.graph.current_graph.TryAddNode(node_name)
        if nodeManager.bad_node_guid == guid:
            raise Exception("Node could not be created: " + node_name)

    def load_cmake_file(self, cmake_file_path : str) -> None:
        self.cmake_compiler.SetCmakeFileLocation(cmake_file_path, False)
        self.cmake_compiler.Compile()
        print("--- Compiling " + cmake_file_path + " ---")
        print(self.cmake_compiler.output_stream)

    def load_gmake_file(self, gmake_file_path : str) -> None:
        __not_implemented__("gmake files don't exist at the time of writing this :)")