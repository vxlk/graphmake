from PyQt5.QtCore import *
import uuid
from model.db.db_module.db_model import *


# Represents a node from the backend, a node will be shown on the front end by a rectangle
class Node(QObject):
    def __init__(self):
        super().__init__()
        self.name = "cmake_version"
        self.code = database.Node(self.name)
        self.guid = uuid.uuid4()
