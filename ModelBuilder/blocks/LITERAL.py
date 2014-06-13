from Block import Block

class LITERAL(Block):

    def __init__(self, node):
        Block.__init__(self, node)

    def add_to_model(self, h):
        vertex = h.add_node()
        h.vs[vertex]['mm__'] = "Constant"
        h.vs[vertex]["value"] = "90"
        self.vertex = vertex
