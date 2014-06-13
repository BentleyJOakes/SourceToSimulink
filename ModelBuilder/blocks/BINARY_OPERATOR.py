from Block import Block

class BINARY_OPERATOR(Block):

    def __init__(self, node):
        Block.__init__(self, node)
        self.value = node.get("TokenKind.PUNCTUATION")

    def __str__(self):
        s = str(self.children[0])
        s += " " + self.value + " "
        s += str(self.children[1])
        return s



    # elif node_kind == "CursorKind.BINARY_OPERATOR" or node_kind == "CursorKind.UNARY_OPERATOR":
    # operator = node.get('TokenKind.PUNCTUATION')
    #
    #     # this is an assignment statement
    #     if operator == "=":
    #         print("Is assignment")
    #
    #         #TODO: This will definitely break in the future
    #         var_name = ''
    #         for child in node:
    #             assert child.get('kind') == "CursorKind.DECL_REF_EXPR", "Assignment operator needs to be fixed"
    #             var_name = child.get('TokenKind.IDENTIFIER')
    #             break
    #
    #         block_num, _ = child_results[1]
    #
    #         #make sure to copy
    #         symbol_table = symbol_table.copy()
    #         symbol_table.update({var_name: block_num})
    #
    #         return block_num, symbol_table
    #
    #     vertex = self.h.add_node()
    #     self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Operator"
    #     self.h.vs[vertex]["value"] = operator
    #
    #     block_num1, _ = child_results[0]
    #     self.h.add_edge(block_num1, vertex)
    #
    #     if len(child_results) > 1:
    #         block_num2, _ = child_results[1]
    #         self.h.add_edge(block_num2, vertex)
    #
    #     return vertex, symbol_table
    #

    def add_to_model(self, h):
        for child in self.children:
            child.symbol_table = self.symbol_table
            child.add_to_model(h)

        vertex = h.add_node()
        h.vs[vertex]['mm__'] = "Binary Operator"
        h.vs[vertex]['value'] = self.value
        self.vertex = vertex

        for child in self.children:
            h.add_edge(vertex, child.vertex)

        self.collect_childrens_symbol_table()
