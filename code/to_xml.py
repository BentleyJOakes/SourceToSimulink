import xml.etree.cElementTree as ET

def write_xml(program):
    root = ET.Element("root")

    write_node(program, root)
    
    tree = ET.ElementTree(root)
    tree.write("simple.xml")
    
def write_node(node, parent):
    node_xml = ET.SubElement(parent, str(node['kind']))

    for attrib in node:
        if attrib == "children" or attrib == "tokens":
            continue
            
        if attrib == "spelling" and node[attrib] == None:
            continue
            
        if attrib == "value" and node[attrib] == '':
            continue
            
        #new_node = ET.SubElement(node_xml, "node")
        node_xml.set(attrib, str(node[attrib]))

        
    #child_tokens = get_child_tokens(node)
    #print "Child tokens"  
    #print child_tokens    
    

    for token in node["tokens"]:
        #if token in child_tokens:
        #    continue
    
        #new_node = ET.SubElement(node_xml, "token")
        node_xml.set(str(token.kind), str(token.spelling))
        #node_xml.text = str(token.spelling)
     
    for child in node['children']:
        write_node(child, node_xml)
        
def get_child_tokens(node):
    tokens = []
    for child in node['children']:
        
        for t in child["tokens"]:
            tokens.append(t)
        tokens += get_child_tokens(child)
        
    return tokens
        
        
        
        
        
        
