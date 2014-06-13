from Block import Block

class IF_STMT(Block):

    def __init__(self, node):
        Block.__init__(self, node)


    def add_to_model(self, h):

        print (self.kind + " " + str(self.symbol_table))

        for child in self.children:
            child.symbol_table = self.symbol_table
            child.add_to_model(h)

        vertex = h.add_node()
        h.vs[vertex]['mm__'] = self.kind

        self.vertex = vertex

        for child in self.children:
            h.add_edge(vertex, child.vertex)

        self.collect_childrens_symbol_table()

