from Block import Block

class COMPOUND_STMT(Block):

    def __init__(self, node):
        Block.__init__(self, node)

    # compound statements just collect the symbol tables for lower nodes
    #TODO: Add comments to subsystems?

    def add_to_model(self, h):
        for child in self.children:
            print("before COMPUND DECL: " + str(self.symbol_table))
            child.symbol_table = self.symbol_table
            child.add_to_model(h)
            self.symbol_table = child.symbol_table
            print(child.kind + " COMPUND DECL: " + str(self.symbol_table))

        vertex = h.add_node()
        h.vs[vertex]['mm__'] = "Compound stmt"
        h.vs[vertex]['value'] = " "
        self.vertex = vertex

        for child in self.children:
            h.add_edge(vertex, child.vertex)

        #self.store_in_symbol_table(self.name, vertex)
