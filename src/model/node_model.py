from PyQt5.QtCore import *
import uuid

# Represents a node from the backend, a node will be shown on the front end by a rectangle
class Node(QObject):
    def __init__(self):
        super().__init__()
        self.name = "Node"
        self.code = "Some Cmake Code"
        self.guid = uuid.uuid4()
