from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import diagraph as G

from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q

def prim_mst(my_graph, source):
    if not G.contains_vertex(my_graph, source):
        raise Exception("El vertice source no existe")
    marked = mlp.new_map(G.order(my_graph), 0.7)
    edge_to = mlp.new_map(G.order(my_graph), 0.7)
    dist_to = mlp.new_map(G.order(my_graph), 0.7)
    ipq = pq.new_heap()
    vertices_list = G.vertices(my_graph)
    for i in range(al.size(vertices_list)):
        v = al.get_element(vertices_list, i)
        mlp.put(dist_to, v, float('inf'))
    mlp.put(dist_to, source, 0.0)
    pq.insert(ipq, source, 0.0)
    while not pq.is_empty(ipq):
        v = pq.remove(ipq)
        mlp.put(marked, v, True)
        adjacents_list = G.adjacents(my_graph, v)
        for i in range(al.size(adjacents_list)):
            w = al.get_element(adjacents_list, i)
            e = G.get_edge(my_graph, v, w)
            wt = ed.weight(e)
            if not mlp.contains(marked, w):
                if wt < mlp.get(dist_to, w):
                    mlp.put(dist_to, w, wt)
                    mlp.put(edge_to, w, v)
                    pq.insert(ipq, w, wt)
    return {'marked': marked, 'edge_to': edge_to, 'dist_to': dist_to}

def edges_mst(my_graph, prim_search):
    if 'edge_to' not in prim_search:
        raise Exception("Prim no ejecutado")
    qres = q.new_queue()
    edge_to_keys = mlp.key_set(prim_search['edge_to'])
    for i in range(al.size(edge_to_keys)):
        v = al.get_element(edge_to_keys, i)
        u = mlp.get(prim_search['edge_to'], v)
        if u is not None:
            edge_weight = ed.weight(G.get_edge(my_graph, u, v))
            q.enqueue(qres, (u, v, edge_weight))
    return qres

def weight_mst(my_graph, prim_search):
    total = 0.0
    edge_to_keys = mlp.key_set(prim_search['edge_to'])
    for i in range(al.size(edge_to_keys)):
        v = al.get_element(edge_to_keys, i)
        u = mlp.get(prim_search['edge_to'], v)
        if u is not None:
            total += ed.weight(G.get_edge(my_graph, u, v))
    return total