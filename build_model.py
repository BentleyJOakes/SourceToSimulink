import xml.etree.ElementTree as ET

from himesis.himesis import Himesis
from himesis.himesis_utils import graph_to_dot


class ModelBuilder:

    def __init__(self):
        self.h = None
        
    def build(self, filename):

        self.h = Himesis(name="simple")
        self.h[Himesis.Constants.META_MODEL] = ['Simulink']
        self.h["name"] = "simple"

        tree = ET.parse(filename)
        root = tree.getroot()

        symbol_table = self.traverse_node(root, None, {})

        print("Symbol Table:")
        print(symbol_table)
        graph_to_dot("simple", self.h, directory = "./examples/")

    def traverse_node(self, node, parent, symbol_table):
        node_kind = node.get('kind')


        #compound statements just collect the symbol tables for lower nodes
        #TODO: Add comments to subsystems?
        if node_kind == "CursorKind.COMPOUND_STMT":
            for child in node:
                _, symbol_table = self.traverse_node(child, node, symbol_table)


            return None, symbol_table

        elif node_kind == 'CursorKind.FUNCTION_DECL':
            for child in node:
                _, symbol_table = self.traverse_node(child, node, symbol_table)


            for key in symbol_table:
                try:
                    float(key)
                    continue

                except ValueError:
                    vertex = self.h.add_node()
                    self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Variable"

                    func_name = node.get('TokenKind.IDENTIFIER')
                    self.h.vs[vertex]["value"] = func_name + " " + key

                    self.h.add_edge(symbol_table[key], vertex)

            return symbol_table


        print(node_kind)
        print("Symbol table:")
        print(symbol_table)

        # all other nodes use a bottom up approach to resolve the symbol tables
        child_results = []
        for child in node:
            child_results.append(self.traverse_node(child, node, symbol_table))

        print(node_kind)
        print("Child results")
        print(child_results)


        #return vertex of constant block with literal
        if node_kind in ["CursorKind.INTEGER_LITERAL", "CursorKind.FLOATING_LITERAL"]:
            literal = node.get('TokenKind.LITERAL')

            # return constant block if already exists
            if literal in symbol_table:
                symbol_table.update({literal: symbol_table[literal]})
                return symbol_table[literal], symbol_table

            #else, create constant block for this literal
            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Constant"
            self.h.vs[vertex]["value"] = literal

            #self.symbol_table[literal] = vertex

            print("Creating: " + str({literal : vertex}))
            symbol_table.update({literal: vertex})
            return vertex, symbol_table

        #set the variable to be set to the child,
        # (the RHS of the declaration) if the variable was given a value
        #otherwise, ignore this variable

        elif node_kind == "CursorKind.VAR_DECL":
            var_name = node.get('spelling')
            #self.symbol_table[var_name] = child_results[0]

            if len(child_results) > 0:
                block_num, _ = child_results[0]
                print("Creating: " + str({var_name : block_num}))
                symbol_table.update({var_name: block_num})
                return block_num, symbol_table
            else:
                print("Returning: " + str(symbol_table))
                return None, symbol_table

        elif node_kind == "CursorKind.DECL_REF_EXPR":
            var_name = node.get('TokenKind.IDENTIFIER')
            block_num = symbol_table[var_name]
            return block_num, symbol_table

        elif node_kind == "CursorKind.BINARY_OPERATOR" or node_kind == "CursorKind.UNARY_OPERATOR":
            operator = node.get('TokenKind.PUNCTUATION')

            # this is an assignment statement
            if operator == "=":
                print("Is assignment")

                #TODO: This will definitely break in the future
                var_name = ''
                for child in node:
                    assert child.get('kind') == "CursorKind.DECL_REF_EXPR", "Assignment operator needs to be fixed"
                    var_name = child.get('TokenKind.IDENTIFIER')
                    break

                block_num, _ = child_results[1]

                #make sure to copy
                symbol_table = symbol_table.copy()
                symbol_table.update({var_name: block_num})

                return block_num, symbol_table

            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Operator"
            self.h.vs[vertex]["value"] = operator

            block_num1, _ = child_results[0]
            self.h.add_edge(block_num1, vertex)

            if len(child_results) > 1:
                block_num2, _ = child_results[1]
                self.h.add_edge(block_num2, vertex)

            return vertex, symbol_table

        elif node_kind == "CursorKind.PARM_DECL":
            # don't know the parent yet, so just create a param block of 1 to represent the in port
            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Param"

            var_name = node.get('spelling')
            self.h.vs[vertex]["value"] = node.get('TokenKind.KEYWORD') + " " + var_name
            symbol_table.update({var_name:vertex})
            return vertex, symbol_table

        elif node_kind == "CursorKind.IF_STMT":
            #vertex = self.h.add_node()
            #self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Switch"


            # self.h.add_edge(child_results[2], vertex)

            children = len(child_results)
            print("IF children: " + str(children))

            print("Symbol table:")
            print(symbol_table)

            switch_value, _ = child_results[0]


            for var_name in symbol_table:
                try:
                    float(var_name)
                    continue

                except ValueError:

                    possible_values = []
                    possible_values.append(symbol_table[var_name])
                    for i in range(1, children):
                        _, child_symbol_table = child_results[i]
                        possible_values.append(child_symbol_table[var_name])

                    print("Possible values")
                    print(set(possible_values))

                    if len(set(possible_values)) > 1:
                        vertex = self.h.add_node()
                        self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Variable Switch"
                        self.h.vs[vertex]['value'] = "Variable is " + var_name

                        self.h.add_edge(switch_value, vertex)

                        for v in set(possible_values):
                            self.h.add_edge(v, vertex)

                        symbol_table = symbol_table.copy()
                        symbol_table.update({var_name:vertex})

            return None, symbol_table

        else:
            print("KIND NOT HANDLED: " + str(node_kind))

        if len(child_results) > 0:
            return child_results[0]
        else:
            return symbol_table
            
            
def main():

    from optparse import OptionParser, OptionGroup

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
    
    
    
    
    
    
    
