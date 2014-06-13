from Block import Block

class PARM_DECL(Block):

    def __init__(self, node):
        Block.__init__(self, node)
        self.name = node.get("spelling")
        self.var_type = node.get("TokenKind.KEYWORD")


    # don't know the parent yet, so just create a param block of 1 to represent the in port
    def add_to_model(self, h):

        assert(len(self.children) == 0, "PARAM has children!")

        vertex = h.add_node()
        h.vs[vertex]['mm__'] = "Param"
        h.vs[vertex]['value'] = self.var_type + " " + self.name
        self.vertex = vertex

        for child in self.children:
            h.add_edge(child.vertex, vertex)

        self.store_in_symbol_table(self.name, vertex)
