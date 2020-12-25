

class Property():
    def __init__(self):
        self.name = ""
        self.type = ""
        self.code = ""
        self.tooltip = ""
        self.editableFields = []

    def AddEditableField(self, typeString):
        self.editableFields.append(typeString)

    # should prob check that it is ok to add
    def ReplaceEditableField(self, fieldIndex, code):
        self.editableFields[fieldIndex] = code