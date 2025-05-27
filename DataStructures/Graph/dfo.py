from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import diagraph as G

from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Stack import stack as s

def dfo(my_graph):
    marked = mlp.new_map(G.order(my_graph), 0.7)
    pre = al.new_list()
    post = al.new_list()
    reversepost = s.new_stack()
    aux = {
        'marked': marked,
        'pre': pre,
        'post': post,
        'reversepost': reversepost
    }
    
    def dfs_vertex(my_graph, v_key, aux):
        mlp.put(aux['marked'], v_key, True)
        al.add_last(aux['pre'], v_key)
        adjacents_list = G.adjacents(my_graph, v_key)
        for i in range(al.size(adjacents_list)):
            w = al.get_element(adjacents_list, i)
            if not mlp.contains(aux['marked'], w) or mlp.get(aux['marked'], w) is None:
                dfs_vertex(my_graph, w, aux)
        al.add_last(aux['post'], v_key)
        s.push(aux['reversepost'], v_key)
    vertices_list = G.vertices(my_graph)
    for i in range(al.size(vertices_list)):
        v_key = al.get_element(vertices_list, i)
        if not mlp.contains(marked, v_key) or mlp.get(marked, v_key) is None:
            dfs_vertex(my_graph, v_key, aux)
    return aux