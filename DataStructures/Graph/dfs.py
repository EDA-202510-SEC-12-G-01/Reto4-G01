from DataStructures.Queue import queue
from DataStructures.Stack import stack
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List.list_iterator import iterator
from DataStructures.Graph import vertex
from DataStructures.Graph import dfo_structure as dfo

def adjacent_vertices(g, key_u):
    if not mp.contains(g['vertices'], key_u):
        raise Exception("El vértice no existe")
    v = mp.get(g['vertices'], key_u)
    return mp.key_set(vertex.get_adjacents(v))

def dfs(my_graph, source):
    g_order = mp.size(my_graph['vertices'])
    search = dfo.new_dfo_structure(g_order)
    search['edge_to'] = mp.new_map(num_elements=g_order, load_factor=0.5)
    search['source'] = source
    dfs_vertex(my_graph, source, search)
    return search

def dfs_vertex(my_graph, key_u, search):
    mp.put(search['marked'], key_u, True)
    queue.enqueue(search['pre'], key_u)
    for neigh in iterator(adjacent_vertices(my_graph, key_u)):
        if not mp.contains(search['marked'], neigh):
            mp.put(search['edge_to'], neigh, key_u)
            dfs_vertex(my_graph, neigh, search)
    queue.enqueue(search['post'], key_u)
    stack.push(search['reversepost'], key_u)
    return search

def has_path_to(key_v, search):
    return mp.contains(search['marked'], key_v)

def path_to(key_v, search):
    if not has_path_to(key_v, search):
        return None
    camino = stack.new_stack()
    current = key_v
    while current != search['source']:
        stack.push(camino, current)
        current = mp.get(search['edge_to'], current)
    stack.push(camino, search['source'])
    return camino