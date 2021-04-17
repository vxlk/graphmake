from PyQt5.QtWidgets import *

from script import ScriptingEngine

# just to make qt happy
app = QApplication([])

# The graphmake test runner
script_engine = ScriptingEngine()

script_engine.add_node("host_system_info")
print(script_engine.current_graph().nodes[0].name)

script_engine.clear()
print(script_engine.current_graph().nodes)

# it seems like load_cmake_file is not filling out the graph
script_engine.load_cmake_file("C:\\Users\\small\\Desktop\\graphmake\\src\\tests\\cmake\\first_example\\CmakeLists.txt")
print(script_engine.current_graph().nodes)
# find tests

# for each folder in tests

# run test in folder