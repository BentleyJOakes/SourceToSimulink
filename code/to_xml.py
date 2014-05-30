import xml.etree.cElementTree as ET

def write_xml(program, name):
    root = ET.Element("root")

    write_node(program, root)
    
    tree = ET.ElementTree(root)
    
    tree.write(name + ".xml")
    
    
#don't store tokens that are really defined for a child node
def compare_tokens(token, tokens):
    for t in tokens:
        if str(token.kind) == str(t.kind) and str(token.spelling) == str(t.spelling):
            return True
            
    return False

def write_node(node, parent):
    node_xml = ET.SubElement(parent, str(node['kind']))
    
    #print(node['kind'])

    for attrib in node:
        if attrib == "children" or attrib == "tokens":
            continue
            
        if attrib == "spelling" and node[attrib] == None:
            continue
            
        if attrib == "value" and node[attrib] == '':
            continue
            
        node_xml.set(attrib, str(node[attrib]))

        
    #child_tokens = get_child_tokens(node) 
    

    for token in node["tokens"]:
        #if compare_tokens(token, child_tokens):
        #    continue
    
        node_xml.set(str(token.kind), str(token.spelling))
     
    for child in node['children']:
        write_node(child, node_xml)
        
def get_child_tokens(node):
    tokens = []
    for child in node['children']:
        for t in child["tokens"]:
            tokens.append(t)
        tokens += get_child_tokens(child)
        
    return tokens
        
        
        
        
        
        
