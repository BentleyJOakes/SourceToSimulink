import xml.etree.ElementTree as ET



from himesis.himesis import Himesis
from himesis.himesis_utils import graph_to_dot
from blocks.BlockCreator import BlockCreator

class ModelBuilder:

    def __init__(self):
        self.h = None
        self.root = None



    def build(self, filename):

        #parse XML to get root
        tree = ET.parse(filename)
        root = tree.getroot()

        #build Python objects for each node
        self.build_structure(root, None)

        #create Himesis graph
        self.h = Himesis(name = "simple")
        self.h[Himesis.Constants.META_MODEL] = ['Simulink']
        self.h["name"] = "simple"

        self.root.add_to_model(self.h)

        print("Symbol Table: " + str(self.root.symbol_table))
        graph_to_dot("simple", self.h, directory = "./examples/")

    def build_structure(self, node, parent):
        block_class = BlockCreator.load_block(node.get("kind"))
        block = block_class(node)

        #save the root block
        if parent is None:
            self.root = block

        #attach all children
        if parent is not None:
            parent.add_child(block)

        block.add_parent(parent)

        for child in node:
            self.build_structure(child, block)






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
        #     return None, symbol_table
        #
        # else:
        #     print("KIND NOT HANDLED: " + str(node_kind))
        #
        # if len(child_results) > 0:
        #     return child_results[0]
        # else:
        #     return symbol_table
            
            
def main():

    from optparse import OptionParser

    global opts

    parser = OptionParser("usage: %prog [options] {filename}")
    
    parser.disable_interspersed_args()
    (opts, args) = parser.parse_args()

    if len(args) == 0:
        parser.error('invalid number arguments')


    filename = args[0]
    
    mb = ModelBuilder()
    mb.build(filename)

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
