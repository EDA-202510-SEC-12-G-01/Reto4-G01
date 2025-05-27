from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import diagraph as G

from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Stack import stack as s

def dijkstra(my_graph, source):
    if not G.contains_vertex(my_graph, source):
        raise Exception("El vertice source no existe")
    dist_to = mlp.new_map(G.order(my_graph), 0.7)
    edge_to = mlp.new_map(G.order(my_graph), 0.7)
    marked = mlp.new_map(G.order(my_graph), 0.7)
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
            if mlp.get(dist_to, v) + wt < mlp.get(dist_to, w):
                mlp.put(dist_to, w, mlp.get(dist_to, v) + wt)
                mlp.put(edge_to, w, v)
                pq.insert(ipq, w, mlp.get(dist_to, w))
    return {'dist_to': dist_to, 'edge_to': edge_to, 'marked': marked}

def dist_to(key_v, dijkstra_search):
    if not mlp.contains(dijkstra_search['dist_to'], key_v):
        raise Exception("El vertice no existe o Dijkstra no ejecutado")
    return mlp.get(dijkstra_search['dist_to'], key_v)

def has_path_to(key_v, dijkstra_search):
    return (mlp.contains(dijkstra_search['dist_to'], key_v) and 
            mlp.get(dijkstra_search['dist_to'], key_v) < float('inf'))

def path_to(key_v, dijkstra_search):
    if not has_path_to(key_v, dijkstra_search):
        return None
    path = s.new_stack()
    v = key_v
    edge_to_map = dijkstra_search['edge_to']
    while mlp.contains(edge_to_map, v) and mlp.get(edge_to_map, v) is not None:
        s.push(path, v)
        v = mlp.get(edge_to_map, v)
    s.push(path, v)
    return path