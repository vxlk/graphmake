from PyQt5.QtCore import *
# scrap this i think, for now skeleton unless things change?
# maybe positions will make this viable
class Connection(QObject):
    def __init__(self):
        super().__init__()
        self.code = ""