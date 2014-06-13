from Block import Block

class DECL_REF_EXPR(Block):

    def __init__(self, node):
        Block.__init__(self, node)
        self.name = node.get("TokenKind.IDENTIFIER")

    def add_to_model(self, h):
        self.vertex = self.symbol_table[self.name]
        self.store_in_symbol_table(self.name, self.vertex)
