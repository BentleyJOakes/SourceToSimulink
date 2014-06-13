from Block import Block

class BINARY_OPERATOR(Block):

    def __init__(self, node):
        Block.__init__(self, node)
        self.value = node.get("TokenKind.PUNCTUATION")

    def add_to_model(self, h):
        for child in self.children:
            child.add_to_model(h)

        vertex = h.add_node()
        h.vs[vertex]['mm__'] = "Binary Operator"
        h.vs[vertex]['value'] = self.value
        self.vertex = vertex

        for child in self.children:
            h.add_edge(vertex, child.vertex)

        self.collect_childrens_symbol_table()
