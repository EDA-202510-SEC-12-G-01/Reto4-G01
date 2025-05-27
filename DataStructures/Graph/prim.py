from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import digraph as G

from DataStructures.List import array_list as al
from DataStructures.List.list_iterator import iterator
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Priority_queue import index_priority_queue as ipq
from DataStructures.Queue import queue as q

def prim_mst(my_graph, source):
    if not G.contains_vertex(my_graph, source):
        raise Exception("El vertice source no existe")
    
    marked = mlp.new_map(G.order(my_graph), 0.7)
    edge_to = mlp.new_map(G.order(my_graph), 0.7)
    dist_to = mlp.new_map(G.order(my_graph), 0.7)
    pq = ipq.new_index_heap(True) 


    for v in iterator(G.vertices(my_graph)):
        mlp.put(dist_to, v, float('inf'))
    

    mlp.put(dist_to, source, 0.0)
    ipq.insert(pq, 0.0, source)

    while not ipq.is_empty(pq):
        v = ipq.remove(pq)
        mlp.put(marked, v, True)
        

        for w in iterator(G.adjacents(my_graph, v)):
            e = G.get_edge(my_graph, v, w)
            wt = ed.weight(e)
            

            if not mlp.contains(marked, w):
                if wt < mlp.get(dist_to, w):
                    mlp.put(dist_to, w, wt)
                    mlp.put(edge_to, w, v)
                    
                    if ipq.contains(pq, w):
                        ipq.decrease_key(pq, w, wt)
                    else:
                        ipq.insert(pq, wt, w)
    
    return {'marked': marked, 'edge_to': edge_to, 'dist_to': dist_to}

def edges_mst(my_graph, prim_search):
    if 'edge_to' not in prim_search:
        raise Exception("Prim no ejecutado")
    
    qres = q.new_queue()
    for v in iterator(mlp.key_set(prim_search['edge_to'])):
        u = mlp.get(prim_search['edge_to'], v)
        if u is not None:
            edge_weight = ed.weight(G.get_edge(my_graph, u, v))
            q.enqueue(qres, (u, v, edge_weight))
    
    return qres

def weight_mst(my_graph, prim_search):
    total = 0.0
    for v in iterator(mlp.key_set(prim_search['edge_to'])):
        u = mlp.get(prim_search['edge_to'], v)
        if u is not None:
            total += ed.weight(G.get_edge(my_graph, u, v))
    return total