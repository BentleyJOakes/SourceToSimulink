from Block import Block

class DECL_STMT(Block):

    def __init__(self, node):
        Block.__init__(self, node)


    def add_to_model(self, h):

        assert len(self.children) == 1, "DECL_STMT doesn't have one child !"

        self.children[0].add_to_model(h)

        self.vertex = self.children[0].vertex

        self.symbol_table.update(self.children[0].symbol_table)
