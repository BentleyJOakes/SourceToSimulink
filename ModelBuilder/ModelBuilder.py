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
    
    
    
    
    
    
    
