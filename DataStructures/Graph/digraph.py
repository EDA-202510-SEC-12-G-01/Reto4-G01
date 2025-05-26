from DataStructures.Map import map_linear_probing as lp
from DataStructures.List import array_list as al
from DataStructures.List.list_iterator import iterator
from DataStructures.Graph import vertex
from DataStructures.Graph import edge

def new_graph(order):
    my_graph = {'vertices': lp.new_map(order, 0.5), 'num_edges': 0}
    return my_graph

def insert_vertex(my_graph, key_u, info_u):
    my_vertex = vertex.new_vertex(key_u, info_u)
    lp.put(my_graph['vertices'], key_u, my_vertex)
    return my_graph

def update_vertex_info(my_graph, key_u, new_info_u):
    if not lp.contains(my_graph['vertices'], key_u):
        return None
    my_vertex = lp.get(my_graph['vertices'], key_u)
    vertex.set_value(my_vertex, new_info_u)
    return my_graph
    
def remove_vertex(my_graph, key_u):
    if not lp.contains(my_graph['vertices'], key_u):
        return None    
    for u_key in iterator(lp.key_set(my_graph['vertices'])):
        if u_key != key_u:
            u = lp.get(my_graph['vertices'], u_key)
            if lp.contains(u['adjacents'], key_u):
                lp.remove(u['adjacents'], key_u)
                my_graph['num_edges'] -= 1

    v = lp.get(my_graph['vertices'], key_u)
    my_graph['num_edges'] -= lp.size(v['adjacents'])

    lp.remove(my_graph['vertices'], key_u)
    return my_graph
    
def add_edge(my_graph, key_u, key_v, weight=1.0):
    if not lp.contains(my_graph['vertices'], key_u):
        raise Exception("El vertice u no existe")
    if not lp.contains(my_graph['vertices'], key_v):
        raise Exception("El vertice v no existe")

    my_vertex = lp.get(my_graph['vertices'], key_u)
    if lp.contains(my_vertex['adjacents'], key_v):
        my_edge = lp.get(my_vertex['adjacents'], key_v)
        edge.set_weight(my_edge, weight)
    else:
        vertex.add_adjacent(my_vertex, key_v, weight)
        my_graph['num_edges'] += 1
    return my_graph

def order(my_graph):
    return lp.size(my_graph['vertices'])

def size(my_graph):
    return my_graph['num_edges']

def vertices(my_graph):
    return lp.key_set(my_graph['vertices'])

def degree(my_graph, key_u):
    if not lp.contains(my_graph['vertices'], key_u):
        raise Exception("El vertice no existe")
    my_vertex = lp.get(my_graph['vertices'], key_u)
    return vertex.degree(my_vertex)

def get_edge(my_graph, key_u, key_v):
    if not lp.contains(my_graph['vertices'], key_u):
        raise Exception("El vertice u no existe")
    u = lp.get(my_graph['vertices'], key_u)
    adj = u['adjacents']
    if not lp.contains(adj, key_v):
        return None
    return lp.get(adj, key_v)

def get_vertex_information(my_graph, key_u):
    if not lp.contains(my_graph['vertices'], key_u):
        raise Exception("El vertice no existe")
    my_vertex = lp.get(my_graph['vertices'], key_u)
    return vertex.get_value(my_vertex)

def contains_vertex(my_graph, key_u):
    return lp.contains(my_graph['vertices'], key_u)

def adjacents(my_graph, key_u):
    if not lp.contains(my_graph['vertices'], key_u):
        raise Exception("El vertice no existe")
    my_vertex = lp.get(my_graph['vertices'], key_u)
    adjacents = vertex.get_adjacents(my_vertex)
    return lp.key_set(adjacents)

def edges_vertex(my_graph, key_u):
    if not lp.contains(my_graph['vertices'], key_u):
        raise Exception("El vertice no existe")
    v = lp.get(my_graph['vertices'], key_u)
    adj_map = v['adjacents']
    edges = al.new_list()
    for neighbor_key in iterator(lp.key_set(adj_map)):
        edge_obj = lp.get(adj_map, neighbor_key)
        al.add_last(edges, edge_obj)
    return edges

def get_vertex(my_graph, key_u):
    if not lp.contains(my_graph['vertices'], key_u):
        raise Exception("El vertice no existe")
    return lp.get(my_graph['vertices'], key_u)