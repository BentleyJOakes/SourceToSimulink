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

        self.symbol_table = self.traverse_node(root, None, 0)
        
        print(self.symbol_table)
        graph_to_dot("simple", self.h, directory = "./examples/")

    def traverse_node(self, node, parent, depth):
        node_kind = node.get('kind')
        child_results = []
        self.symbol_table = {}
        for child in node:
            child_results.append(self.traverse_node(child, node, depth + 1))

        print(node_kind)
        if node_kind in ['XML', 'CursorKind.TYPEDEF_DECL', 'CursorKind.TYPE_REF', 'CursorKind.TRANSLATION_UNIT',
                         'CursorKind.DECL_STMT', 'CursorKind.UNEXPOSED_EXPR']:
            if len(child_results) > 0:
                return child_results[0]
            else:
                return None

        print(child_results)
        if node_kind in ["CursorKind.INTEGER_LITERAL", "CursorKind.FLOATING_LITERAL"]:
            literal = node.get('TokenKind.LITERAL')

            # return constant block if already exists
            if literal in self.symbol_table:
                return self.symbol_table[literal]

            #else, create constant block for this literal
            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Constant"
            self.h.vs[vertex]["value"] = literal

            self.symbol_table[literal] = vertex
            return vertex

        elif node_kind == "CursorKind.VAR_DECL":
            var_name = node.get('spelling')
            self.symbol_table[var_name] = child_results[0]

        elif node_kind == "CursorKind.PARM_DECL":
            # don't know the parent yet, so just create a gain block of 1 to represent the in port
            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Gain"

            var_name = node.get('TokenKind.IDENTIFIER')
            self.h.vs[vertex]["value"] = node.get('TokenKind.KEYWORD') + " " + var_name

            #self.symbol_table[var_name] = vertex

            return vertex

            var_name = node.get('spelling')
            self.symbol_table[var_name] = child_results[0]

        elif node_kind == "CursorKind.DECL_REF_EXPR":
            var_name = node.get('TokenKind.IDENTIFIER')
            return None  # self.symbol_table[var_name]

        elif node_kind == "CursorKind.COMPOUND_STMT":
            # TODO: Place comments in subsystems?
            #            comment = node.get('TokenKind.COMMENT')
            #            
            #            vertex = self.h.add_node()
            #            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Comment"
            #            self.h.vs[vertex]["value"] = comment
            #            
            #            self.h.add_edge(child_results[0], vertex)
            #            
            #            return vertex
            pass

        elif node_kind == "CursorKind.IF_STMT":
            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Switch"

            self.h.add_edge(child_results[0], vertex)
            self.h.add_edge(child_results[1], vertex)
            # self.h.add_edge(child_results[2], vertex)

            return vertex


        elif node_kind == "CursorKind.BINARY_OPERATOR" or node_kind == "CursorKind.UNARY_OPERATOR":
            operator = node.get('TokenKind.PUNCTUATION')

            if operator == "=":
                # this is an assignment statement
                pass

            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Operator"
            self.h.vs[vertex]["value"] = operator

            self.h.add_edge(child_results[0], vertex)

            if len(child_results) > 1:
                self.h.add_edge(child_results[1], vertex)

            return vertex

        else:
            print("KIND NOT HANDLED: " + str(node_kind))
        if len(child_results) > 0:
            return child_results[0]
        else:
            return None
            
            
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
    
    
    
    
    
    
    
