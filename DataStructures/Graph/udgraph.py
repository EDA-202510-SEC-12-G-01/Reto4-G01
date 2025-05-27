from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.List.list_iterator import iterator
from DataStructures.Graph import vertex
from DataStructures.Graph import edge


def new_graph(order):
    return {'vertices': mp.new_map(order, 0.5), 'num_edges': 0}

def insert_vertex(my_graph, key_u, info_u):
    my_vertex = vertex.new_vertex(key_u, info_u)
    mp.put(my_graph['vertices'], key_u, my_vertex)
    return my_graph

def update_vertex_info(my_graph, key_u, new_info_u):
    if not mp.contains(my_graph['vertices'], key_u):
        return None
    my_vertex = mp.get(my_graph['vertices'], key_u)
    vertex.set_value(my_vertex, new_info_u)
    return my_graph

def remove_vertex(my_graph, key_u):
    if not mp.contains(my_graph['vertices'], key_u):
        return None
    v = mp.get(my_graph['vertices'], key_u)
    neighbor_keys = list(mp.key_set(vertex.get_adjacents(v)))
    for nk in neighbor_keys:
        neighbor = mp.get(my_graph['vertices'], nk)
        if mp.contains(vertex.get_adjacents(neighbor), key_u):
            neighbor['adjacents'] = mp.remove(vertex.get_adjacents(neighbor), key_u)
            my_graph['num_edges'] -= 1
    mp.remove(my_graph['vertices'], key_u)
    return my_graph

def add_edge(my_graph, key_u, key_v, weight=1.0):
    if key_u == key_v:
        raise Exception("No se permiten self-loops")
    if not mp.contains(my_graph['vertices'], key_u):
        raise Exception("El vértice u no existe")
    if not mp.contains(my_graph['vertices'], key_v):
        raise Exception("El vértice v no existe")
    u = mp.get(my_graph['vertices'], key_u)
    v = mp.get(my_graph['vertices'], key_v)
    u_adj = vertex.get_adjacents(u)
    v_adj = vertex.get_adjacents(v)
    if mp.contains(u_adj, key_v):
        e_uv = mp.get(u_adj, key_v)
        e_vu = mp.get(v_adj, key_u)
        edge.set_weight(e_uv, weight)
        edge.set_weight(e_vu, weight)
    else:
        vertex.add_adjacent(u, key_v, weight)
        vertex.add_adjacent(v, key_u, weight)
        my_graph['num_edges'] += 1
    return my_graph

def remove_edge(my_graph, key_u, key_v):
    if key_u == key_v:
        raise Exception("No se permiten self-loops")
    if not mp.contains(my_graph['vertices'], key_u):
        raise Exception("El vértice u no existe")
    if not mp.contains(my_graph['vertices'], key_v):
        raise Exception("El vértice v no existe")
    u = mp.get(my_graph['vertices'], key_u)
    v = mp.get(my_graph['vertices'], key_v)
    u_adj = vertex.get_adjacents(u)
    v_adj = vertex.get_adjacents(v)
    if mp.contains(u_adj, key_v):
        u['adjacents'] = mp.remove(u_adj, key_v)
        v['adjacents'] = mp.remove(v_adj, key_u)
        my_graph['num_edges'] -= 1
    return my_graph

def order(my_graph):
    return mp.size(my_graph['vertices'])

def size(my_graph):
    return my_graph['num_edges']

def vertices(my_graph):
    return mp.key_set(my_graph['vertices'])

def degree(my_graph, key_u):
    if not mp.contains(my_graph['vertices'], key_u):
        raise Exception("El vértice no existe")
    v = mp.get(my_graph['vertices'], key_u)
    return vertex.degree(v)

def get_edge(my_graph, key_u, key_v):
    if not mp.contains(my_graph['vertices'], key_u):
        raise Exception("El vértice u no existe")
    u = mp.get(my_graph['vertices'], key_u)
    return mp.get(vertex.get_adjacents(u), key_v)

def get_vertex_information(my_graph, key_u):
    if not mp.contains(my_graph['vertices'], key_u):
        raise Exception("El vértice no existe")
    v = mp.get(my_graph['vertices'], key_u)
    return vertex.get_value(v)

def contains_vertex(my_graph, key_u):
    return mp.contains(my_graph['vertices'], key_u)

def adjacents(my_graph, key_u):
    if not mp.contains(my_graph['vertices'], key_u):
        raise Exception("El vértice no existe")
    v = mp.get(my_graph['vertices'], key_u)
    return mp.key_set(vertex.get_adjacents(v))

def edges_vertex(my_graph, key_u):
    if not mp.contains(my_graph['vertices'], key_u):
        raise Exception("El vértice no existe")
    v = mp.get(my_graph['vertices'], key_u)
    edges = al.new_list()
    for nk in iterator(mp.key_set(vertex.get_adjacents(v))):
        al.add_last(edges, mp.get(vertex.get_adjacents(v), nk))
    return edges

def get_vertex(my_graph, key_u):
    if not mp.contains(my_graph['vertices'], key_u):
        raise Exception("El vértice no existe")
    return mp.get(my_graph['vertices'], key_u)