import xml.etree.ElementTree as ET

from himesis import Himesis
from himesis_utils import graph_to_dot

class ModelBuilder:

    def __init__(self):
        self.symbol_table = {}
        self.h = None

        #HACK: Needed for binary operator, as children eat the operator token
        self.punctuation_seen = []
        
    def build(self, filename):

        self.h = Himesis(name="simple")
        self.h[Himesis.Constants.META_MODEL] = ['Simulink']
        self.h["name"] = "simple"


        tree = ET.parse(filename)
        root = tree.getroot()

        self.traverse_node(root, None)
        
        print(self.symbol_table)
        graph_to_dot("simple", self.h)



    def traverse_node(self, node, parent):

        node_kind = node.get('kind')
        
        
     
        child_results = []
        
        for child in node:
            child_results.append(self.traverse_node(child, node))
            
        print(node_kind)
        print(child_results)    
        
        
        punct = node.get('TokenKind.PUNCTUATION')
        if not punct == None:
            self.punctuation_seen.append(punct)
                   
        if node_kind in ["CursorKind.INTEGER_LITERAL", "CursorKind.FLOATING_LITERAL"]:
            literal = node.get('TokenKind.LITERAL')
            
            #return constant block if already exists
            if literal in self.symbol_table:
                return self.symbol_table[literal] 
            
            #create constant block for this literal
            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = "Constant"
            self.h.vs[vertex]["value"] = literal
            
            self.symbol_table[literal] = vertex
            return vertex
               
        elif node_kind == "CursorKind.VAR_DECL":
            var_name = node.get('spelling')
            self.symbol_table[var_name] = child_results[0]
            
        elif node_kind == "CursorKind.DECL_REF_EXPR":
            var_name = node.get('TokenKind.IDENTIFIER')
            return self.symbol_table[var_name]
            
            
        elif node_kind == "CursorKind.BINARY_OPERATOR":
            
            p = None
            
            #TODO: Make this pretty
            while len(self.punctuation_seen) > 0:
                p = self.punctuation_seen.pop()

                if p in [';', '=', '(', ')']:
                    continue
                    
                break

            if p == None:
                print("ERROR: BINARY OPERATOR DOES NOT HAVE AN OPERATOR")
                
            
            #create constant block for this literal
            vertex = self.h.add_node()
            self.h.vs[vertex][Himesis.Constants.META_MODEL] = p
            
            self.h.add_edge(child_results[0], vertex)
            self.h.add_edge(child_results[1], vertex)
            
            return vertex   
            
        if len(child_results) > 0:    
            return child_results[0]
        else:
            return None
            
            
def main():

    filename = "simple.c.xml"
    
    mb = ModelBuilder()
    mb.build(filename)

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
