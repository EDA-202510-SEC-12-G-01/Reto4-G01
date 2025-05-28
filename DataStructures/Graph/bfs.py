# En tu DataStructures/Graph/bfs.py

from DataStructures.Queue import queue
from DataStructures.Stack import stack
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.List.list_iterator import iterator
from DataStructures.Graph import vertex
from DataStructures.Graph import udgraph as gr
from DataStructures.Utils import error  # si lo necesitas


def bfs(my_graph, source):
    order = gr.order(my_graph)
    search = {
        'marked': mp.new_map(order, 0.5),
        'edge_to': mp.new_map(order, 0.5),
        'dist_to': mp.new_map(order, 0.5),
        'source': source
    }
    return bfs_vertex(my_graph, source, search)

def bfs_vertex(my_graph, source, vmap):
    mp.put(vmap['marked'], source, True)
    mp.put(vmap['dist_to'], source, 0)

    q = queue.new_queue()
    queue.enqueue(q, source)

    while not queue.is_empty(q):
        u = queue.dequeue(q)
        neighs = gr.adjacents(my_graph, u)
        al.merge_sort(neighs, al.default_sort_criteria)
        for v in iterator(neighs):
            if not mp.contains(vmap['marked'], v):
                mp.put(vmap['marked'], v, True)
                mp.put(vmap['edge_to'], v, u)
                dist_u = mp.get(vmap['dist_to'], u)
                mp.put(vmap['dist_to'], v, dist_u + 1)
                queue.enqueue(q, v)
    return vmap

def has_path_to(vertex, vmap):
    return mp.contains(vmap['marked'], vertex)

def path_to(vertex, vmap):
    if not has_path_to(vertex, vmap):
        return None
    camino = stack.new_stack()
    cur = vertex
    while cur != vmap['source']:
        stack.push(camino, cur)
        cur = mp.get(vmap['edge_to'], cur)
    stack.push(camino, vmap['source'])
    return camino
