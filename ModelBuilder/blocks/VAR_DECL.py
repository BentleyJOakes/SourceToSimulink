from Block import Block

class VAR_DECL(Block):

    def __init__(self, node):
        Block.__init__(self, node)
        self.name = node.get("spelling")
        self.var_type = node.get("TokenKind.KEYWORD")

    # #set the variable to be set to the child,
    # # (the RHS of the declaration) if the variable was given a value
    # #otherwise, ignore this variable
    #
    # elif node_kind == "CursorKind.VAR_DECL":
    # var_name = node.get('spelling')
    #     #self.symbol_table[var_name] = child_results[0]
    #
    #     if len(child_results) > 0:
    #         block_num, _ = child_results[0]
    #         print("Creating: " + str({var_name : block_num}))
    #         symbol_table.update({var_name: block_num})
    #         return block_num, symbol_table
    #     else:
    #         print("Returning: " + str(symbol_table))
    #         return None, symbol_table
    #

    def add_to_model(self, h):

        assert len(self.children) == 1, "VAR_DECL doesn't have one child !"

        self.children[0].add_to_model(h)

        self.vertex = self.children[0].vertex
        self.symbol_table = self.children[0].symbol_table
        self.store_in_symbol_table(self.name, self.vertex)
