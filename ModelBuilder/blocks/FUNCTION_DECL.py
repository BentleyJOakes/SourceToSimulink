from Block import Block

class FUNCTION_DECL(Block):

    def __init__(self, node):
        Block.__init__(self, node)
        self.name = node.get("spelling")
        self.return_type = node.get("TokenKind.KEYWORD")


    def add_to_model(self, h):

        for child in self.children:
            child.symbol_table = self.symbol_table
            child.add_to_model(h)
            self.symbol_table = child.symbol_table

        vertex = h.add_node()
        h.vs[vertex]['mm__'] = "Subsystem"
        h.vs[vertex]['value'] = self.return_type + " " + self.name
        self.vertex = vertex

        for child in self.children:
            h.add_edge(child.vertex, vertex)


        #
        # for key in symbol_table:
        # try:
        # float(key)
        #         continue
        #
        #     except ValueError:
        #         vertex = self.h.add_node()
        #         self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Variable"
        #
        #         func_name = node.get('TokenKind.IDENTIFIER')
        #         self.h.vs[vertex]["value"] = func_name + " " + key
        #
        #         self.h.add_edge(symbol_table[key], vertex)
        #
        # return symbol_table
        #
