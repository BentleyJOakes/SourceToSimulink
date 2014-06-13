from Block import Block

class LITERAL(Block):
    # #return vertex of constant block with literal
    # if node_kind in ["CursorKind.INTEGER_LITERAL", "CursorKind.FLOATING_LITERAL"]:
    # literal = node.get('TokenKind.LITERAL')
    #
    #     # return constant block if already exists
    #     if literal in symbol_table:
    #         symbol_table.update({literal: symbol_table[literal]})
    #         return symbol_table[literal], symbol_table
    #
    #     #else, create constant block for this literal
    #     vertex = self.h.add_node()
    #     self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Constant"
    #     self.h.vs[vertex]["value"] = literal
    #
    #     #self.symbol_table[literal] = vertex
    #
    #     print("Creating: " + str({literal : vertex}))
    #     symbol_table.update({literal: vertex})
    #     return vertex, symbol_table
    #
    def __init__(self, node):
        Block.__init__(self, node)
        self.value = node.get("TokenKind.LITERAL")

    def __str__(self):
        return self.value

    def add_to_model(self, h):
        vertex = h.add_node()
        h.vs[vertex]['mm__'] = "Constant"
        h.vs[vertex]['value'] = self.value
        self.vertex = vertex

        self.store_in_symbol_table(self.value, vertex)
