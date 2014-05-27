'''
Created on 2013-01-21

@author: levi
'''

'''
Useful Himesis-related operations

'''

import pydot
import subprocess
import re

from copy import deepcopy


#used to check if a constraint has been left as default
#note that all whitespace is removed to increase accuracy
default_constraint = re.sub(r'\s+', '', """
#===============================================================================
# This code is executed when evaluating if a node shall be matched by this rule.
# You can access the value of the current node's attribute value by: attr_value.
# You can access any attribute x of this node by: this['x'].                    
# If the constraint relies on attribute values from other nodes,                
# use the LHS/NAC constraint instead.                                           
# The given constraint must evaluate to a boolean expression.                   
#===============================================================================
                                                                                
return True                                                                     
""")

def get_attribute(s, attr):
    #remove whitespace to check against the default_constraint
    if re.sub(r'\s+', '', str(attr)) == default_constraint:
        return ""
    else:
        return s + str(attr)

def graph_to_dot(name, g, verbosity = 0):
    """
    build a dot file from a himesis graph
    verbosity = 0, no traceability in the dot graph
    verbosity = 1, traceability in the dot graph
    """
    
    if g == None:
        print("graph_to_dot Error: Empty graph")
        return 
        
    vattr=''
    nodes = {}
    graph = pydot.Dot(name, graph_type='digraph')
    #print("graph_to_dot: " + str(g))
    
    #print("===================================================\n")
    for i in range(len(g.vs)):
    #for v in g.vs:
        #print(v)
        #print("============\n")
    
        v = g.vs[i]
        
        node_type = str(v['mm__'])
        node_GUID = str(v['GUID__'])[-12:]
        
        vattr += str(i) + " - "
        vattr += node_type
        #vattr += node_GUID
        
        try:
            label = str(v["MT_label__"])
            vattr += "\\n Label " + label
        except Exception:
            pass
                
        fillcolor = "lightblue"
        
        if '__Contains__' in node_type:
            fillcolor="lightgray"  
            
        elif 'SubSystem' in node_type:
            
                
            fillcolor="lightgreen"  
                       
        elif node_type in ['Port_Output']:
            fillcolor="coral"          
                 
        elif node_type in ['Port_Input']:
            fillcolor="lightyellow" 
            
        elif node_type in ['Inport', 'Outport']:
            fillcolor="lightgoldenrod"
            
        elif node_type in ['__Block_Outport__', '__Block_Inport__']:
            fillcolor="#b94a62"
            
        elif node_type in ['__Relation__']:
            fillcolor="#f78465"
            #if  verbosity == 1:
              #  nodes[v.index] = pydot.Node(vattr, style="filled", fillcolor="chocolate")
              
              
        else:
            try:
                vattr += "\\n Classtype = " + str(v['classtype'])
            except Exception:
                pass
                
            try:
                vattr += "\\n Name = " + str(v['name'])
            except Exception:
                pass
                
            if 'MT_pre__classtype' in v.attributes():
                vattr += get_attribute("\\n Classtype = ", v['MT_pre__classtype'])
                
            if 'MT_pre__name' in v.attributes():
                vattr += get_attribute("\\n Name = ", v['MT_pre__name'])

                
            if 'value' in v.attributes() and not v['value'] == None:
                vattr += get_attribute("\\n Value = ", v['value'])

                
            if 'gain' in v.attributes() and not v['gain'] == None:
                vattr += get_attribute("\\n Gain = ", v['gain'])

                
            fillcolor="lightblue"
                
        nodes[v.index] = pydot.Node(vattr, style="filled", fillcolor=fillcolor)
        graph.add_node(nodes[v.index])  
        
        vattr = ''
        
        
        
        
    for e in g.es:
        
        #correct the direction of input lines
        #if ("Input" in g.vs[e.target]['mm__'] or "Inport" in g.vs[e.target]['mm__']) and not "__Relation__" in g.vs[e.source]['mm__']:
        #    graph.add_edge(pydot.Edge(nodes[e.target],nodes[e.source]))
        #else:
        graph.add_edge(pydot.Edge(nodes[e.source],nodes[e.target]))

    dot_filename = './dot/' + name + '.dot'
    graph.write(dot_filename)
    
    command = "dot -Tsvg " + dot_filename + " -o " + dot_filename.replace(".dot", ".svg")
    #print(command)
    subprocess.call(command, shell=True)
#    graph.write('/home/gehan/OutputDotFiles/%s.dot'%name)    

def disjoint_model_union(first, second):
    """
    merge two himesis graphs
    IMPORTANT: only makes sense if the graphs are instances of the same metamodel
    """
    
    nr_attr_first = len(first.vs[0].attribute_names())
    nr_attr_second = len(second.vs[0].attribute_names())
    
    # graphs need to be swapped in case the nodes in the second graph have more attributes than the ones in the first
    # this is so because each node in a model has the maximum amount of attributes used in the model
    
    if nr_attr_second > nr_attr_first:
        swapbuffer = deepcopy(second)
        second = deepcopy(first)
        first = swapbuffer

    # get the list of attributes to copy from the second graph but don't copy the GUIDs because they are newly created        
    attribute_names = [attr for attr in second.vs[0].attribute_names() if attr != 'GUID__']
    nb_nodes_first = len(first.vs)
    
    # first copy the nodes
    for index_v in range(len(second.vs)):
        first.add_node()
        for attr_name in attribute_names:
            first.vs[nb_nodes_first + index_v][attr_name] = second.vs[index_v][attr_name]

    # then copy the edges
    for index_e in range(len(second.es)):
        first.add_edges((nb_nodes_first + second.es[index_e].tuple[0],nb_nodes_first + second.es[index_e].tuple[1]))
        
    first.name = first.name + '-' + second.name
 
    return first
    
def disjoint_union_two_models(first, second):
    """
    merge two himesis graphs
    IMPORTANT: only makes sense if the graphs are instances of the same metamodel
    """
    
    nr_attr_first = len(first.vs[0].attribute_names())
    nr_attr_second = len(second.vs[0].attribute_names())
    
    # graphs need to be swapped in case the nodes in the second graph have more attributes than the ones in the first
    # this is so because each node in a model has the maximum amount of attributes used in the model
    
    if nr_attr_second > nr_attr_first:
        swapbuffer = deepcopy(second)
        second = deepcopy(first)
        first = swapbuffer

    # get the list of attributes to copy from the second graph but don't copy the GUIDs because they are newly created        
    attribute_names = [attr for attr in second.vs[0].attribute_names() if attr != 'GUID__']
    nb_nodes_first = len(first.vs)
    
    # first copy the nodes
    for index_v in range(len(second.vs)):
        first.add_node()
        for attr_name in attribute_names:
            first.vs[nb_nodes_first + index_v][attr_name] = second.vs[index_v][attr_name]

    # then copy the edges
    for index_e in range(len(second.es)):
        first.add_edges((nb_nodes_first + second.es[index_e].tuple[0],nb_nodes_first + second.es[index_e].tuple[1]))
        
    first.name = first.name + '-' + second.name
 
    return first


def disjoint_model_union(model_list):
    """
    merge several himesis graphs
    IMPORTANT: only makes sense if the graphs are instances of the same metamodel
    """ 
    # go through all the rules in the layer and merge them in one graph

    merged_models = deepcopy(model_list[0])
    for model_index in range(1,len(model_list)):
        merged_models = disjoint_union_two_models(merged_models, model_list[model_index])

    return merged_models


def print_graph(graph):
    """
    pretty print a Himesis graph
    """
    # first print the nodes
    print 'Name: ' + graph.name
    
    print 'Nodes: '
    for v in graph.vs:
        print v
    
    # then print the edges
    print 'Edges: '
    for e in graph.es:
        print e  
