import xml.etree.ElementTree as ET

from himesis import Himesis
from himesis_utils import graph_to_dot

def build_model(filename):

    h = Himesis(name="simple")
    h[Himesis.Constants.META_MODEL] = ['Simulink']
    h["name"] = "simple"

    tree = ET.parse(filename)
    root = tree.getroot()

    print_node(h, root, None)
    
    graph_to_dot("simple", h)

def print_node(h, node, parent):
    vertex = h.add_node()
    
    h.vs[vertex][Himesis.Constants.META_MODEL] = str(node.get('kind'))
    h.vs[vertex][str(node.tag)] = str(node.attrib)
    
    if not parent == None: 
        h.add_edge(parent, vertex)
    
    for child in node:
        print_node(h, child, vertex)

def main():

    filename = "simple.xml"
    build_model(filename)

if __name__ == '__main__':
    main()
