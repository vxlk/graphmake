
# a connection represents a "connection" between 2 nodes
# (node a. and node b.) a. will have an output and b. will
# have an input.  output can be piped into input, this cannot
# be done the other way
# a variable definition will always have an output (that can be
# the input to many different nodes)

class Input:
    def __init__(self):

class Output:
    def __init__(self):

class Connection:
    def __init__(self):
        #vars go here
        self.input = Input()
        self.output = Input()
        self.nodeName = "empty node name"
        