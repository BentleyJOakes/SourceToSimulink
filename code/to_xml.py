import xml.etree.cElementTree as ET

def write_xml(program, name):
    root = ET.Element("root")

    write_node(program, root)
    
    tree = ET.ElementTree(root)
    
    tree.write(name + ".xml")
    
    


def write_node(node, parent):

    node_xml = ET.SubElement(parent, str(node['kind']))
    
    used_tokens = []
    for child in node['children']:
        used_tokens += write_node(child, node_xml)
        
    #get unique set of tokens
    tokens = node['tokens']
    for t in used_tokens:
        tokens.remove(t)
    
    for attrib in node:
        if attrib == "children" or attrib == "tokens":
            continue
            
        if attrib == "spelling" and node[attrib] == None:
            continue
        
        if attrib == "location" and node[attrib] == None:
            continue
            
        node_xml.set(attrib, str(node[attrib]))

    
    node_kind = str(node['kind'])
    print(node_kind)
    
    tokens_to_use = []
    if "LITERAL" in node_kind:
        tokens_to_use.append(remove_token_kind("TokenKind.LITERAL", tokens))
    
    elif node_kind == "CursorKind.DECL_REF_EXPR":
        tokens_to_use.append(remove_token_kind("TokenKind.IDENTIFIER", tokens))
        
    elif node_kind == "CursorKind.BINARY_OPERATOR":
        tokens_to_use.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        
    elif node_kind == "CursorKind.VAR_DECL":
        tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens))
        tokens_to_use.append(remove_token_kind("TokenKind.IDENTIFIER", tokens))
        
    elif node_kind == "CursorKind.DECL_STMT":
        #remove '=' and ';' but don't output to XML
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        
    elif node_kind == "CursorKind.COMPOUND_STMT":
        #remove '{' and '}' but don't output to XML
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        
    elif node_kind == "CursorKind.FUNCTION_DECL":
        tokens_to_use.append(remove_token_kind("TokenKind.KEYWORD", tokens))
        tokens_to_use.append(remove_token_kind("TokenKind.IDENTIFIER", tokens))
        
        #TODO: Need to handle arguements
        #remove '{' and '}' but don't output to XML
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        used_tokens.append(remove_token_kind("TokenKind.PUNCTUATION", tokens))
        
    #mark the token as consumed and output it to XML
    for t in tokens_to_use:    
        node_xml.set(t.kind, t.spelling)
        used_tokens.append(t)
        
        print("\tFound: " + str(t))
        
        
    for t in tokens:
        print("\t\t" + str(t))
    
    return used_tokens
    

def remove_token_kind(kind, tokens, reverse = False):
    if reverse:
        tokens = reversed(tokens)

    for t in tokens:
        if t.kind == kind:
            tokens.remove(t)
            return t
    return None
        
        
