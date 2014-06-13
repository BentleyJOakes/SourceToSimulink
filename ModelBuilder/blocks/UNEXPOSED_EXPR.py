from Block import Block

class UNEXPOSED_EXPR(Block):

    def __init__(self, node):
        Block.__init__(self, node)

    def __str__(self):
        return str(self.children[0])

    def add_to_model(self, h):

        assert len(self.children) == 1, "UNEXPOSED_EXPR doesn't have one child !"

        self.children[0].symbol_table = self.symbol_table
        self.children[0].add_to_model(h)

        self.vertex = self.children[0].vertex

        self.symbol_table.update(self.children[0].symbol_table)
