from DataStructures.Queue import queue
from DataStructures.Stack import stack
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List.list_iterator import iterator
from DataStructures.Graph import vertex  # para acceder a las adyacencias

def _adjacent_vertices(g, key_u):
    if not mp.contains(g['vertices'], key_u):
        raise Exception("El vértice no existe")
    v = mp.get(g['vertices'], key_u)
    return mp.key_set(vertex.get_adjacents(v))

def bfs(my_graph, source):
    g_order = mp.size(my_graph['vertices'])
    vmap = {
        'marked': mp.new_map(g_order, 0.5),
        'edge_to': mp.new_map(g_order, 0.5),
        'dist_to': mp.new_map(g_order, 0.5),
        'source': source
    }
    bfs_vertex(my_graph, source, vmap)
    return vmap

def bfs_vertex(my_graph, source, vmap):
    q = queue.new_queue()
    mp.put(vmap['marked'], source, True)
    mp.put(vmap['dist_to'], source, 0)
    queue.enqueue(q, source)
    while not queue.is_empty(q):
        u = queue.dequeue(q)
        for neigh in iterator(_adjacent_vertices(my_graph, u)):
            if not mp.contains(vmap['marked'], neigh):
                mp.put(vmap['marked'], neigh, True)
                mp.put(vmap['edge_to'], neigh, u)
                mp.put(vmap['dist_to'], neigh, mp.get(vmap['dist_to'], u) + 1)
                queue.enqueue(q, neigh)
    return vmap

def has_path_to(key_v, vmap):
    return mp.contains(vmap['marked'], key_v)


def path_to(key_v, vmap):
    if not has_path_to(key_v, vmap):
        return None
    camino = stack.new_stack()
    current = key_v
    while current != vmap['source']:
        stack.push(camino, current)
        current = mp.get(vmap['edge_to'], current)
    stack.push(camino, vmap['source'])
    return camino
