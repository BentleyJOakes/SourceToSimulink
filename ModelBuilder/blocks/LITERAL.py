from Block import Block

class LITERAL(Block):

    def __init__(self, node):
        Block.__init__(self, node)
        self.value = node.get("TokenKind.LITERAL")

    def add_to_model(self, h):
        vertex = h.add_node()
        h.vs[vertex]['mm__'] = "Constant"
        h.vs[vertex]['value'] = self.value
        self.vertex = vertex

        self.store_in_symbol_table(self.value, vertex)
