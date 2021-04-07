from PyQt5.QtWidgets import *

from script import ScriptingEngine

# just to make qt happy
app = QApplication([])

# The graphmake test runner
script_engine = ScriptingEngine()

script_engine.add_node("host_system_info")
print(script_engine.graph.current_graph.nodes[0].name)
# find tests

# for each folder in tests

# run test in folder