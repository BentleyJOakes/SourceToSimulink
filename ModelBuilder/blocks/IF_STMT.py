from Block import Block
from COMPOUND_STMT import COMPOUND_STMT

class IF_STMT(Block):

    def __init__(self, node):
        Block.__init__(self, node)





        # elif node_kind == "CursorKind.IF_STMT":
        #     #vertex = self.h.add_node()
        #     #self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Switch"
        #
        #
        #     # self.h.add_edge(child_results[2], vertex)
        #
        #     children = len(child_results)
        #     print("IF children: " + str(children))
        #
        #     print("Symbol table:")
        #     print(symbol_table)
        #
        #     switch_value, _ = child_results[0]
        #
        #
        #     for var_name in symbol_table:
        #         try:
        #             float(var_name)
        #             continue
        #
        #         except ValueError:
        #
        #             possible_values = []
        #             possible_values.append(symbol_table[var_name])
        #             for i in range(1, children):
        #                 _, child_symbol_table = child_results[i]
        #                 possible_values.append(child_symbol_table[var_name])
        #
        #             print("Possible values")
        #             print(set(possible_values))
        #
        #             if len(set(possible_values)) > 1:
        #                 vertex = self.h.add_node()
        #                 self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Variable Switch"
        #                 self.h.vs[vertex]['value'] = "Variable is " + var_name
        #
        #                 self.h.add_edge(switch_value, vertex)
        #
        #                 for v in set(possible_values):
        #                     self.h.add_edge(v, vertex)
        #
        #                 symbol_table = symbol_table.copy()
        #                 symbol_table.update({var_name:vertex})
        #

    def add_to_model(self, h):

        print (self.kind + " " + str(self.symbol_table))

        conditions = []
        self.get_condition(conditions)
        print(conditions)

        print(self.children[0])


        print(self.children[1].kind)
        for child in self.children:
            child.symbol_table = self.symbol_table
            child.add_to_model(h)

        vertex = h.add_node()
        h.vs[vertex]['mm__'] = self.kind

        self.vertex = vertex

        for child in self.children:
            h.add_edge(vertex, child.vertex)

        self.collect_childrens_symbol_table()

    def get_condition(self, conditions):
        conditions.append(str(self.children[0]))
        if len(self.children) == 3:

            if isinstance(self.children[2], IF_STMT):
                self.children[2].get_condition(conditions)
            elif isinstance(self.children[2], COMPOUND_STMT):
                conditions.append('')

